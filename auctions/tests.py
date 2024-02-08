"""Unit tests"""
from django.test import TestCase
from .models import Bid, Listing, User
from .myforms import ListingForm, CommentForm

class BidModelTestCase(TestCase):
    """Test for valid bids"""
    def setUp(self):
        self.user1 = User.objects.create_user(username='user1', password='password123')
        self.user2 = User.objects.create_user(username='user2', password='password123')
        self.listing = Listing.objects.create (
            seller=self.user1, itemname='Test Item',
            price=50.00, description='Test description',
            image='https://example.com/image.jpg',
            category='1')
        self.bid1 = Bid.objects.create(name=self.user2, bid=60.00, item=self.listing)

    def test_next_bid_higher(self):
        """Ensure that next bid placed is higher than the previous"""
        # Create a new bid that is higher than the previous bid
        new_bid_higher = Bid(name=self.user2, bid=70.00, item=self.listing)
        self.assertTrue(new_bid_higher.bid > self.bid1.bid)

        # Create a new bid that is lower than the previous bid
        new_bid_lower = Bid(name=self.user2, bid=55.00, item=self.listing)
        self.assertFalse(new_bid_lower.bid > self.bid1.bid)

class ListingFormTestCase(TestCase):
    """Test for a valid listing"""
    def test_listing_form_valid_data(self):
        """Valid form test"""
        form = ListingForm(data={
            'thetitle': 'Test Item',
            'thedescription': 'Test description',
            'theprice': 50.00,
            'thepicture': 'https://example.com/image.jpg',
            'thecategory': '1'
        })
        self.assertTrue(form.is_valid())

    def test_listing_form_invalid_data(self):
        """Invalid form test"""
        form = ListingForm(data={})
        self.assertFalse(form.is_valid())

    def test_listing_form_valid_data2(self):
        "Invalid form test"
        #Test for invalid price entry
        form = ListingForm(data={
            'thetitle': 'Test Item',
            'thedescription': 'Test description',
            'theprice': "Five",
            'thepicture': 'https://example.com/image.jpg',
            'thecategory': '1'
        })
        self.assertFalse(form.is_valid())

class CommentTestCase(TestCase):
    """Test for valid comments"""
    def test_comment1(self):
        """Empty comment test"""
        form = CommentForm(data={
            'thecomment' : ""
        })
        self.assertFalse(form.is_valid())

    def test_comment2(self):
        """Valid comment test"""
        form = CommentForm(data={
            'thecomment' : "Nice!"
        })
        self.assertTrue(form.is_valid())
