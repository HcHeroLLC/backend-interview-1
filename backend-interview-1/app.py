# Marketing Campaign API - Scaffolding
#
# This API manages marketing campaigns for an organization.
# Some endpoints are implemented, others need to be completed.

from flask import Flask, request, jsonify
from dataclasses import dataclass, asdict
from typing import Optional
import uuid

app = Flask(__name__)


@dataclass
class Campaign:
    """Represents a marketing campaign."""
    id: str
    name: str
    owner_email: str
    channel: str
    goal: str
    parent_campaign_id: Optional[str] = None


# In-memory storage
campaigns_db: dict[str, Campaign] = {}


def seed_data():
    """Populate the database with sample campaigns."""
    sample_campaigns = [
        Campaign(
            id="camp-001",
            name="Q4 Product Launch",
            owner_email="sarah.chen@cascade.ai",
            channel="Multi-channel",
            goal="Drive awareness for the v3 launch",
            parent_campaign_id=None
        ),
        Campaign(
            id="camp-002",
            name="Launch Email Nurture",
            owner_email="marcus.j@cascade.ai",
            channel="Email",
            goal="Convert trial signups to paid",
            parent_campaign_id="camp-001"
        ),
        Campaign(
            id="camp-003",
            name="Launch Paid Social",
            owner_email="emily.r@cascade.ai",
            channel="Paid Social",
            goal="Generate 500 launch-week signups",
            parent_campaign_id="camp-001"
        ),
        Campaign(
            id="camp-004",
            name="SEO Content Refresh",
            owner_email="david.kim@cascade.ai",
            channel="Content",
            goal="Grow organic traffic 20%",
            parent_campaign_id=None
        ),
        Campaign(
            id="camp-005",
            name="Annual Customer Summit",
            owner_email="lisa.wang@cascade.ai",
            channel="Events",
            goal="Expand accounts through customer advocacy",
            parent_campaign_id=None
        ),
    ]

    for campaign in sample_campaigns:
        campaigns_db[campaign.id] = campaign


# =============================================================================
# Health Check
# =============================================================================

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Docker."""
    return jsonify({"status": "healthy", "campaign_count": len(campaigns_db)})


# =============================================================================
# Implemented Endpoints
# =============================================================================

@app.route('/campaigns', methods=['GET'])
def list_campaigns():
    """
    List all campaigns.

    Returns:
        JSON array of all campaigns
    """
    return jsonify([asdict(campaign) for campaign in campaigns_db.values()])


@app.route('/campaigns', methods=['POST'])
def create_campaign():
    """
    Create a new campaign.

    Expected JSON body:
        - name (required): Campaign name
        - owner_email (required): Email address of the campaign owner
        - channel (required): Marketing channel (e.g. Email, Paid Social, Events)
        - goal (required): What the campaign is meant to achieve
        - parent_campaign_id (optional): ID of the parent campaign

    Returns:
        The created campaign with generated ID
    """
    data = request.get_json()

    # Validate required fields
    required_fields = ['name', 'owner_email', 'channel', 'goal']
    missing_fields = [f for f in required_fields if f not in data]

    if missing_fields:
        return jsonify({
            'error': 'Missing required fields',
            'missing': missing_fields
        }), 400

    # Validate parent campaign exists if provided
    if data.get('parent_campaign_id') and data['parent_campaign_id'] not in campaigns_db:
        return jsonify({'error': 'Parent campaign not found'}), 400

    campaign = Campaign(
        id=f"camp-{uuid.uuid4().hex[:8]}",
        name=data['name'],
        owner_email=data['owner_email'],
        channel=data['channel'],
        goal=data['goal'],
        parent_campaign_id=data.get('parent_campaign_id')
    )

    campaigns_db[campaign.id] = campaign
    return jsonify(asdict(campaign)), 201


@app.route('/campaigns/<campaign_id>', methods=['GET'])
def get_campaign(campaign_id):
    """
    Get a single campaign by ID.

    Returns:
        The campaign if found, 404 otherwise
    """
    if campaign_id not in campaigns_db:
        return jsonify({'error': 'Campaign not found'}), 404

    return jsonify(asdict(campaigns_db[campaign_id]))


# =============================================================================
# TODO: Implement these endpoints
# =============================================================================

@app.route('/campaigns/<campaign_id>', methods=['PATCH'])
def update_campaign(campaign_id):
    """
    Update an existing campaign.

    TODO: Implement this endpoint

    Requirements:
        - Return 404 if campaign not found
        - Accept partial updates (only update fields that are provided)
        - Validate parent_campaign_id if provided
        - Return the updated campaign
    """
    # YOUR CODE HERE
    return jsonify({'error': 'Not implemented'}), 501


@app.route('/campaigns/<campaign_id>', methods=['DELETE'])
def delete_campaign(campaign_id):
    """
    Delete a campaign.

    TODO: Implement this endpoint

    Requirements:
        - Return 404 if campaign not found
        - Consider: What should happen to sub-campaigns of this campaign?
        - Return appropriate success response
    """
    # YOUR CODE HERE
    return jsonify({'error': 'Not implemented'}), 501


# =============================================================================
# Extension endpoints (implement if time permits)
# =============================================================================

# TODO: Add search functionality to GET /campaigns
#       e.g., GET /campaigns?channel=Email&q=summit

# TODO: Add pagination to GET /campaigns
#       e.g., GET /campaigns?page=1&per_page=10

# TODO: Add endpoint to get sub-campaigns
#       e.g., GET /campaigns/<id>/subcampaigns


if __name__ == '__main__':
    seed_data()
    print(f"Seeded {len(campaigns_db)} campaigns")
    app.run(host='0.0.0.0', port=5050, debug=True)
