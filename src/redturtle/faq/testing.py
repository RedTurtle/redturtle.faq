# -*- coding: utf-8 -*-
from plone.app.contenttypes.testing import PLONE_APP_CONTENTTYPES_FIXTURE
from plone.app.robotframework.testing import REMOTE_LIBRARY_BUNDLE_FIXTURE
from plone.app.testing import (
    applyProfile,
    FunctionalTesting,
    IntegrationTesting,
    PloneSandboxLayer,
)
from plone.testing import z2

import redturtle.faq


class RedturtleFaqLayer(PloneSandboxLayer):

    defaultBases = (PLONE_APP_CONTENTTYPES_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load any other ZCML that is required for your tests.
        # The z3c.autoinclude feature is disabled in the Plone fixture base
        # layer.
        import plone.restapi
        self.loadZCML(package=plone.restapi)
        self.loadZCML(package=redturtle.faq)

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'redturtle.faq:default')


REDTURTLE_FAQ_FIXTURE = RedturtleFaqLayer()


REDTURTLE_FAQ_INTEGRATION_TESTING = IntegrationTesting(
    bases=(REDTURTLE_FAQ_FIXTURE,),
    name='RedturtleFaqLayer:IntegrationTesting',
)


REDTURTLE_FAQ_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(REDTURTLE_FAQ_FIXTURE,),
    name='RedturtleFaqLayer:FunctionalTesting',
)


REDTURTLE_FAQ_ACCEPTANCE_TESTING = FunctionalTesting(
    bases=(
        REDTURTLE_FAQ_FIXTURE,
        REMOTE_LIBRARY_BUNDLE_FIXTURE,
        z2.ZSERVER_FIXTURE,
    ),
    name='RedturtleFaqLayer:AcceptanceTesting',
)
