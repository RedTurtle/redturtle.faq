# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from plone import api
from plone.restapi.serializer.converters import json_compatible
from redturtle.faq.interfaces import IFaq
from redturtle.faq.interfaces import IFaqFolder
from redturtle.faq.interfaces import IRedturtleFaqLayer
from redturtle.faq.interfaces import ISerializeFaqToJsonSummary
from zope.component import adapter
from zope.component import getMultiAdapter
from zope.interface import implementer
from plone.restapi.blocks import visit_blocks, iter_block_transform_handlers
from plone.restapi.interfaces import IBlockFieldSerializationTransformer
from copy import deepcopy


@implementer(ISerializeFaqToJsonSummary)
@adapter(IFaq, IRedturtleFaqLayer)
class FaqSummarySerializer(object):
    """
    This is not the standard summary serializer because we want also blocks.
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        obj = aq_inner(self.context)
        result = {
            "@id": obj.absolute_url(),
            "id": obj.id,
            "title": obj.title,
            "description": obj.description,
            "@type": obj.portal_type,
            "created": json_compatible(obj.created()),
            "modified": json_compatible(obj.modified()),
            "UID": obj.UID(),
        }
        blocks = getattr(obj, "blocks", {})
        if blocks:
            result["blocks"] = self.serialize_blocks(blocks=blocks)
            result["blocks_layout"] = getattr(obj, "blocks_layout", [])

        return result

    def serialize_blocks(self, blocks):
        """
        Return serialized blocks
        """
        value = deepcopy(blocks)

        for block in visit_blocks(self.context, value):
            new_block = block.copy()
            for handler in iter_block_transform_handlers(
                self.context, block, IBlockFieldSerializationTransformer
            ):
                new_block = handler(new_block)
            block.clear()
            block.update(new_block)
        return json_compatible(value)


@implementer(ISerializeFaqToJsonSummary)
@adapter(IFaqFolder, IRedturtleFaqLayer)
class FaqFolderSummarySerializer(FaqSummarySerializer):
    """
    This is not the standard summary serializer because we want alsoits children.
    """

    def __call__(self):
        faqs = self.get_faqs()
        if not faqs:
            # do not show this folder
            return {}
        result = super(FaqFolderSummarySerializer, self).__call__()
        result["icon"] = getattr(self.context, "icon", "")
        result["items"] = faqs
        return result

    def get_faqs(self):
        children = self.context.listFolderContents(
            contentFilter={"portal_type": ["Faq", "FaqFolder"]}
        )
        query = self._build_query()
        catalog = api.portal.get_tool(name="portal_catalog")
        brains = catalog(**query)
        faq_uids = [x.UID for x in brains]
        res = []
        if not brains:
            # there are no faqs in this folder or none that match the search
            return res
        for child in children:
            if child.portal_type == "Faq" and child.UID() not in faq_uids:
                # this not meet the search
                continue
            data = getMultiAdapter((child, self.request), ISerializeFaqToJsonSummary)()
            if data:
                res.append(data)
        return res

    def _build_query(self):
        path = "/".join(self.context.getPhysicalPath())
        query = {
            "path": path,
            "portal_type": "Faq",
        }
        if "SearchableText" in self.request.form:
            query["SearchableText"] = self.request.form["SearchableText"]
        return query
