# BidBay
E-commerce like auction site

A video demo can be located [here](https://youtu.be/q6ccLMdzZT8?si=8LrgcayLzAHciRRC)

![BidBay Image:](https://github.com/zerrynlh/BidBay/blob/main/auctions/static/images/bidbay3.png)

### Description:
This project is a web-based application called Bidbay that allows users to post listings and place bids.

The backend for this application was written using Python and the web framework Django. Information is stored in a PostgreSQL database. Docker was utilized for containerization.

#### Install dependencies:
>pip install -r requirements.txt

#### To run this application:
>python manage.py runserver

### Features:
- Create Listing: users can create a listing by providing details such as an image URL, starting price, description, etc.
- Active Listings: users can view active listings on the homepage.
- Watchlist: users can add and remove items from their watchlist.
- Categories: users can filter by category.
