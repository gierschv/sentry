# -*- coding: utf-8 -*-

from __future__ import absolute_import

import six

from sentry.api.serializers import serialize
from sentry.testutils import TestCase
from sentry.models import Authenticator, UserEmail
from sentry.models.authenticator import available_authenticators


class UserSerializerTest(TestCase):
    def test_simple(self):
        user = self.create_user()

        result = serialize(user)
        assert result['id'] == six.text_type(user.id)
        assert result['has2fa'] is False

        Authenticator.objects.create(
            user=user,
            type=available_authenticators(ignore_backup=True)[0].type,
        )

        useremail = UserEmail.objects.create(
            user=user,
            email='stebe@example.com',
            is_verified=True,
        )

        result = serialize(user)
        assert result['id'] == six.text_type(user.id)
        assert result['has2fa'] is True
        assert len(result['emails']) == 2. # Primary email + new secondary email
        assert result['emails'][0]['email'] == user.email
        assert result['emails'][1] == {
            'id': six.text_type(useremail.id),
            'email': 'stebe@example.com',
            'is_verified': True,
        }
