# Test suite for Marketing Campaign API
#
# Run with: pytest tests/ -v

import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, campaigns_db, seed_data


@pytest.fixture
def client():
    """Create a test client."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        # Reset and seed data before each test
        campaigns_db.clear()
        seed_data()
        yield client


class TestExistingEndpoints:
    """Tests for already-implemented endpoints."""

    def test_health_check(self, client):
        response = client.get('/health')
        assert response.status_code == 200
        assert response.json['status'] == 'healthy'

    def test_list_campaigns(self, client):
        response = client.get('/campaigns')
        assert response.status_code == 200
        assert len(response.json) == 5

    def test_get_campaign(self, client):
        response = client.get('/campaigns/camp-001')
        assert response.status_code == 200
        assert response.json['name'] == 'Q4 Product Launch'

    def test_get_campaign_not_found(self, client):
        response = client.get('/campaigns/nonexistent')
        assert response.status_code == 404

    def test_create_campaign(self, client):
        response = client.post('/campaigns', json={
            'name': 'Test Campaign',
            'owner_email': 'test@cascade.ai',
            'channel': 'Email',
            'goal': 'Test the API'
        })
        assert response.status_code == 201
        assert response.json['name'] == 'Test Campaign'
        assert 'id' in response.json


class TestUpdateCampaign:
    """Tests for PATCH /campaigns/<id> - Candidate implements this."""

    def test_update_campaign_full(self, client):
        """Update all fields of a campaign."""
        response = client.patch('/campaigns/camp-002', json={
            'name': 'Launch Email Nurture v2',
            'owner_email': 'marcus.johnson@cascade.ai',
            'channel': 'Lifecycle Email',
            'goal': 'Re-engage churned trials',
            'parent_campaign_id': 'camp-004'
        })
        assert response.status_code == 200
        assert response.json['name'] == 'Launch Email Nurture v2'
        assert response.json['channel'] == 'Lifecycle Email'

    def test_update_campaign_partial(self, client):
        """Update only some fields (partial update)."""
        response = client.patch('/campaigns/camp-002', json={
            'goal': 'Convert 10% of trial signups to paid'
        })
        assert response.status_code == 200
        assert response.json['goal'] == 'Convert 10% of trial signups to paid'
        # Other fields should remain unchanged
        assert response.json['name'] == 'Launch Email Nurture'
        assert response.json['channel'] == 'Email'

    def test_update_campaign_not_found(self, client):
        """Return 404 for non-existent campaign."""
        response = client.patch('/campaigns/nonexistent', json={
            'name': 'Nothing'
        })
        assert response.status_code == 404

    def test_update_campaign_invalid_parent(self, client):
        """Reject update with non-existent parent_campaign_id."""
        response = client.patch('/campaigns/camp-002', json={
            'parent_campaign_id': 'nonexistent'
        })
        assert response.status_code == 400


class TestDeleteCampaign:
    """Tests for DELETE /campaigns/<id> - Candidate implements this."""

    def test_delete_campaign(self, client):
        """Successfully delete a campaign."""
        response = client.delete('/campaigns/camp-003')
        assert response.status_code in [200, 204]

        # Verify campaign is gone
        response = client.get('/campaigns/camp-003')
        assert response.status_code == 404

    def test_delete_campaign_not_found(self, client):
        """Return 404 for non-existent campaign."""
        response = client.delete('/campaigns/nonexistent')
        assert response.status_code == 404

    def test_delete_campaign_count_decreases(self, client):
        """Campaign count should decrease after deletion."""
        response = client.get('/campaigns')
        initial_count = len(response.json)

        client.delete('/campaigns/camp-003')

        response = client.get('/campaigns')
        assert len(response.json) == initial_count - 1


class TestExtensions:
    """Tests for extension tasks (optional)."""

    @pytest.mark.skip(reason="Extension: Search functionality")
    def test_search_by_channel(self, client):
        response = client.get('/campaigns?channel=Email')
        assert response.status_code == 200
        for campaign in response.json:
            assert campaign['channel'] == 'Email'

    @pytest.mark.skip(reason="Extension: Search functionality")
    def test_search_by_name(self, client):
        response = client.get('/campaigns?q=summit')
        assert response.status_code == 200
        assert len(response.json) == 1
        assert 'Summit' in response.json[0]['name']

    @pytest.mark.skip(reason="Extension: Pagination")
    def test_pagination(self, client):
        response = client.get('/campaigns?page=1&per_page=2')
        assert response.status_code == 200
        assert len(response.json['items']) == 2
        assert 'total' in response.json
        assert 'page' in response.json

    @pytest.mark.skip(reason="Extension: Sub-campaigns")
    def test_get_subcampaigns(self, client):
        response = client.get('/campaigns/camp-001/subcampaigns')
        assert response.status_code == 200
        # Q4 Product Launch (camp-001) has 2 sub-campaigns
        assert len(response.json) == 2
