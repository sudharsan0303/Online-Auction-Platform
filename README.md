# **Online Auction Platform**

The **Online Auction Platform** is a web application designed to enable users to create auctions, place bids, and manage items in a secure and user-friendly environment. Built using **Flask**, **SQLite**, and other modern web technologies like **HTML**, **CSS**, and **JavaScript**, this platform supports both sellers and buyers, offering real-time bidding functionality.

## **Features**
- **User Registration & Login**: Secure user login system for buyers and sellers.
- **Auction Creation**: Sellers can list items for auction with a description, starting bid, and auction end date.
- **Bidding System**: Buyers can place bids on items. The highest bid is displayed in real time.
- **Admin Dashboard**: Admins can manage auctions and users from an easy-to-use dashboard.
- **Bid History**: Track all bids placed for an auction.
- **Responsive Design**: Access the platform on desktop and mobile devices.

## **Installation**

### **1. Install Python:**
   - Download and install Python from [Python.org](https://www.python.org/downloads/).

### **2. Clone the Repository:**
   - Clone the repository to your local machine:
     ```bash
     git clone https://github.com/your-username/online-auction-platform.git
     ```

### **3. Navigate to Project Folder:**
   - Open the project folder in VS Code or your preferred code editor.

### **4. Install Required Dependencies:**
   - In the terminal, run the following command to install the required dependencies:
     ```bash
     pip install -r requirements.txt
     ```

## **Running the Application**

1. **Check Database Files:**
   - Ensure the following databases exist in the `data` folder:
     - `user_data.db` for user information.
     - `auction.db` for auction data.
     - `bids.db` for bid history.

   - If any of the databases are missing, run the respective setup script to create them:
     - `setup_user_database.py`
     - `setup_auction_database.py`
     - `setup_bids_database.py`

2. **Start the Application:**
   - Run the application using:
     ```bash
     python app.py
     ```

   - Alternatively, right-click the `app.py` file and select **Run in Terminal**.

## **Access the Application**

- Once the app is running, open your browser and navigate to:


- Use the application from your browser.

## **File Structure**


## **Contributing**

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-name`).
3. Commit your changes (`git commit -m 'Add new feature'`).
4. Push to your branch (`git push origin feature-name`).
5. Open a Pull Request.

## **License**
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## **Acknowledgments**
- **Flask** is used to create the web framework.
- **SQLite** for lightweight database storage.
- **HTML/CSS** for front-end design.
