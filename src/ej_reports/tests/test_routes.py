import csv
import io

import numpy as np
import pytest
from django.http import QueryDict
from django.test import RequestFactory

from ej.testing import UrlTester
from ej_conversations.mommy_recipes import ConversationRecipes
from ej_reports.routes import index, clusters, radar, divergence, map_to_table
from ej_users.models import User
from .examples import REPORT_RESPONSE, CSV_OUT, MAP_TO_TABLE

BASE_URL = '/api/v1'


class TestRoutes(ConversationRecipes, UrlTester):
    owner_urls = [
        '/conversations/conversation/reports/',
        '/conversations/conversation/reports/clusters/',
        '/conversations/conversation/reports/radar/',
        '/conversations/conversation/reports/divergence/',
    ]

    @pytest.fixture
    def data(self, conversation, author_db):
        conversation.author = author_db
        conversation.save()


class TestReportRoutes(ConversationRecipes):
    @pytest.fixture
    def request_factory(self):
        return RequestFactory()

    @pytest.fixture
    def admin_user(self, db):
        admin_user = User.objects.create_superuser('admin@test.com', 'pass')
        admin_user.save()
        yield admin_user
        admin_user.delete()

    @pytest.fixture
    def request_as_admin(self, request_factory, admin_user):
        request = request_factory
        request.user = admin_user
        return request

    def test_report_route(self, request_as_admin, mk_conversation):
        conversation = mk_conversation()
        path = BASE_URL + f'/conversations/{conversation.slug}/reports/'
        request = request_as_admin
        request.GET = QueryDict('')
        request.get(path)
        response = index(request, conversation)

        assert REPORT_RESPONSE['statistics'] in response.values()

    def test_report_csv_route(self, request_as_admin, mk_conversation):
        conversation = mk_conversation()
        path = BASE_URL + f'/conversations/{conversation.slug}/reports/'
        request = request_as_admin
        request.GET = QueryDict('action=generate_csv')
        request.get(path)
        response = index(request, conversation)

        assert response.status_code == 200

        content = response.content.decode('utf-8')
        csv.reader(io.StringIO(content))
        assert CSV_OUT['votes_header'] in content
        assert CSV_OUT['votes_content'] in content
        assert CSV_OUT['comments_header'] in content
        assert CSV_OUT['comments_content'] in content
        assert CSV_OUT['advanced_comments_header'] in content
        assert CSV_OUT['advanced_participants_header'] in content

    def test_clusters_route(self, mk_conversation):
        conversation = mk_conversation
        response = clusters(conversation)
        expected = {
            'conversation': conversation,
        }

        assert response == expected

    def test_radar_route(self, mk_conversation):
        conversation = mk_conversation
        response = radar(conversation)
        expected = {
            'conversation': conversation,
        }

        assert response == expected

    def test_divergence_route(self, mk_conversation):
        conversation = mk_conversation
        response = divergence(conversation)
        expected = {
            'conversation': conversation,
        }

        assert response == expected

    def test_map_to_table(self, mk_conversation):
        statistics = mk_conversation().statistics()
        mapped_votes = map_to_table(statistics['votes'])

        assert np.array_equal(MAP_TO_TABLE, mapped_votes)
