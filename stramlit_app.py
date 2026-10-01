import streamlit as st
from datetime import date
from gtts import gTTS
import random
import string
import os

# ---------------------------------------------------------
# PAGE CONFIG
# ---------------------------------------------------------

st.set_page_config(
    page_title="MovieBook",
    page_icon="🎬",
    layout="wide"
)

# ---------------------------------------------------------
# SESSION STATE
# ---------------------------------------------------------

if "bookings" not in st.session_state:
    st.session_state.bookings = []

if "booking_confirmed" not in st.session_state:
    st.session_state.booking_confirmed = False

if "current_booking" not in st.session_state:
    st.session_state.current_booking = None


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

movies = {
    "Avengers: Endgame": {
        "language": "English",
        "genre": "Action / Adventure",
        "duration": "3h 1m"
    },
    "Interstellar": {
        "language": "English",
        "genre": "Sci-Fi / Drama",
        "duration": "2h 49m"
    },
    "3 Idiots": {
        "language": "Hindi",
        "genre": "Comedy / Drama",
        "duration": "2h 50m"
    },
    "Kantara": {
        "language": "Kannada",
        "genre": "Action / Drama",
        "duration": "2h 28m"
    },
    "Pushpa 2": {
        "language": "Telugu",
        "genre": "Action",
        "duration": "3h 20m"
    }
}

cinemas = {
    "PVR Cinemas": {
        "location": "City Centre",
        "shows": ["10:00 AM", "1:30 PM", "5:00 PM", "8:30 PM"]
    },
    "INOX": {
        "location": "Mall Road",
        "shows": ["11:00 AM", "2:30 PM", "6:00 PM", "9:30 PM"]
    },
    "Cinepolis": {
        "location": "Phoenix Mall",
        "shows": ["10:30 AM", "1:45 PM", "5:15 PM", "8:45 PM"]
    }
}

seat_prices = {
    "Silver": 180,
    "Gold": 250,
    "Premium": 350
}

food_items = {
    "Regular Popcorn": 180,
    "Large Popcorn": 280,
    "Cheese Popcorn": 320,
    "Coke": 120,
    "Pepsi": 120,
    "Nachos": 220,
    "Combo - Popcorn + Coke": 350
}


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.title("🎬 MovieBook")

st.caption("Movie ticket booking application")

st.divider()


# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("📍 Location")

    city = st.selectbox(
        "Select City",
        [
            "Pune",
            "Mumbai",
            "Solapur",
            "Bengaluru",
            "Hyderabad"
        ]
    )

    st.divider()

    st.header("👤 Account")

    customer_name = st.text_input(
        "Your Name",
        placeholder="Enter your name"
    )

    mobile = st.text_input(
        "Mobile Number",
        placeholder="10 digit mobile number"
    )


# ---------------------------------------------------------
# MAIN TABS
# ---------------------------------------------------------

tab_booking, tab_history = st.tabs(
    ["🎟️ Book Tickets", "📜 Booking History"]
)


# =========================================================
# BOOKING TAB
# =========================================================

with tab_booking:

    # -----------------------------------------------------
    # MOVIE
    # -----------------------------------------------------

    st.header("🎬 Select Movie")

    movie = st.selectbox(
        "Choose a movie",
        list(movies.keys())
    )

    movie_info = movies[movie]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.info(f"🌐 Language\n\n{movie_info['language']}")

    with col2:
        st.info(f"🎭 Genre\n\n{movie_info['genre']}")

    with col3:
        st.info(f"⏱️ Duration\n\n{movie_info['duration']}")


    st.divider()


    # -----------------------------------------------------
    # DATE
    # -----------------------------------------------------

    st.header("📅 Select Date")

    booking_date = st.date_input(
        "Movie date",
        min_value=date.today()
    )


    st.divider()


    # -----------------------------------------------------
    # CINEMA
    # -----------------------------------------------------

    st.header("🏢 Select Cinema")

    cinema = st.selectbox(
        "Choose cinema",
        list(cinemas.keys())
    )

    cinema_info = cinemas[cinema]

    st.caption(
        f"📍 {cinema_info['location']}, {city}"
    )


    # -----------------------------------------------------
    # SHOWTIME
    # -----------------------------------------------------

    st.subheader("🕐 Select Showtime")

    show_time = st.radio(
        "Available shows",
        cinema_info["shows"],
        horizontal=True
    )


    st.divider()


    # -----------------------------------------------------
    # SEAT CATEGORY
    # -----------------------------------------------------

    st.header("💺 Select Seat Category")

    seat_category = st.radio(
        "Seat type",
        list(seat_prices.keys()),
        horizontal=True
    )

    seat_price = seat_prices[seat_category]

    st.write(
        f"**{seat_category} Seat:** ₹{seat_price}"
    )


    # -----------------------------------------------------
    # SEAT MAP
    # -----------------------------------------------------

    st.subheader("🎟️ Select Your Seats")

    st.caption(
        "Screen"
    )

    st.markdown(
        """
        <div style="
            text-align:center;
            padding:10px;
            border-radius:10px;
            background:#eeeeee;
            margin-bottom:20px;
        ">
        🎥 SCREEN
        </div>
        """,
        unsafe_allow_html=True
    )

    selected_seats = []

    seat_rows = {
        "A": 8,
        "B": 8,
        "C": 10,
        "D": 10,
        "E": 10,
        "F": 10
    }

    for row, number_of_seats in seat_rows.items():

        cols = st.columns(number_of_seats)

        for index in range(number_of_seats):

            seat_number = f"{row}{index + 1}"

            with cols[index]:

                selected = st.checkbox(
                    str(index + 1),
                    key=f"seat_{row}_{index}"
                )

                if selected:
                    selected_seats.append(seat_number)

        st.caption(f"Row {row}")


    number_of_seats = len(selected_seats)

    ticket_amount = number_of_seats * seat_price


    st.write(
        f"Selected seats: **{', '.join(selected_seats) if selected_seats else 'None'}**"
    )

    st.write(
        f"Ticket amount: **₹{ticket_amount}**"
    )


    st.divider()


    # -----------------------------------------------------
    # FOOD & BEVERAGES
    # -----------------------------------------------------

    st.header("🍿 Food & Beverages")

    add_food = st.checkbox(
        "Add Food & Beverages"
    )

    food_total = 0
    selected_food = []

    if add_food:

        for item, price in food_items.items():

            quantity = st.number_input(
                f"{item} - ₹{price}",
                min_value=0,
                max_value=10,
                value=0,
                step=1,
                key=f"food_{item}"
            )

            if quantity > 0:

                selected_food.append(
                    f"{item} x {quantity}"
                )

                food_total += price * quantity


    # -----------------------------------------------------
    # OFFER
    # -----------------------------------------------------

    st.divider()

    st.header("🎁 Apply Offer")

    promo_code = st.text_input(
        "Promo Code",
        placeholder="Try MOVIE100"
    )

    discount = 0

    if promo_code:

        if promo_code.upper() == "MOVIE100":

            if ticket_amount >= 500:

                discount = 100

                st.success(
                    "🎉 ₹100 discount applied!"
                )

            else:

                st.warning(
                    "Minimum ticket value ₹500 required."
                )

        elif promo_code.upper() == "FIRST50":

            discount = min(50, ticket_amount)

            st.success(
                "🎉 ₹50 discount applied!"
            )

        else:

            st.error(
                "Invalid promo code"
            )


    # -----------------------------------------------------
    # PAYMENT / ORDER SUMMARY
    # -----------------------------------------------------

    st.divider()

    st.header("🧾 Order Summary")

    convenience_fee = 0

    if number_of_seats > 0:

        convenience_fee = number_of_seats * 25

    subtotal = (
        ticket_amount
        + food_total
        + convenience_fee
    )

    final_amount = max(
        0,
        subtotal - discount
    )


    col1, col2 = st.columns(2)

    with col1:

        st.write("🎟️ Tickets")
        st.write(f"₹{ticket_amount}")

        st.write("🍿 Food")
        st.write(f"₹{food_total}")

        st.write("💳 Convenience Fee")
        st.write(f"₹{convenience_fee}")

        st.write("🎁 Discount")
        st.write(f"- ₹{discount}")

    with col2:

        st.metric(
            "Total Amount",
            f"₹{final_amount}"
        )


    st.divider()


    # -----------------------------------------------------
    # PAYMENT
    # -----------------------------------------------------

    st.header("💳 Payment")

    payment_method = st.radio(
        "Select payment method",
        [
            "UPI",
            "Credit / Debit Card",
            "Net Banking",
            "Wallet"
        ],
        horizontal=True
    )


    if payment_method == "UPI":

        upi_id = st.text_input(
            "UPI ID",
            placeholder="example@upi"
        )

    elif payment_method == "Credit / Debit Card":

        card_number = st.text_input(
            "Card Number",
            type="password",
            placeholder="XXXX XXXX XXXX XXXX"
        )

        card_name = st.text_input(
            "Card Holder Name"
        )

        col1, col2 = st.columns(2)

        with col1:
            expiry = st.text_input(
                "Expiry",
                placeholder="MM/YY"
            )

        with col2:
            cvv = st.text_input(
                "CVV",
                type="password"
            )


    # -----------------------------------------------------
    # BOOK BUTTON
    # -----------------------------------------------------

    st.divider()

    if st.button(
        "🎟️ Proceed to Pay",
        type="primary",
        use_container_width=True
    ):

        if not customer_name:

            st.error(
                "Please enter your name."
            )

        elif not mobile:

            st.error(
                "Please enter your mobile number."
            )

        elif len(mobile) != 10 or not mobile.isdigit():

            st.error(
                "Please enter a valid 10 digit mobile number."
            )

        elif not selected_seats:

            st.error(
                "Please select at least one seat."
            )

        else:

            # Generate booking ID

            booking_id = (
                "MB"
                + "".join(
                    random.choices(
                        string.ascii_uppercase
                        + string.digits,
                        k=8
                    )
                )
            )


            booking = {

                "booking_id": booking_id,

                "name": customer_name,

                "mobile": mobile,

                "city": city,

                "movie": movie,

                "cinema": cinema,

                "date": str(booking_date),

                "show": show_time,

                "seats": selected_seats,

                "seat_category": seat_category,

                "food": selected_food,

                "ticket_amount": ticket_amount,

                "food_amount": food_total,

                "convenience_fee": convenience_fee,

                "discount": discount,

                "total": final_amount,

                "payment": payment_method
            }


            st.session_state.bookings.append(
                booking
            )

            st.session_state.current_booking = booking

            st.session_state.booking_confirmed = True


    # =====================================================
    # CONFIRMATION
    # =====================================================

    if st.session_state.booking_confirmed:

        booking = st.session_state.current_booking

        st.divider()

        st.success(
            "🎉 Booking Confirmed!"
        )

        st.header("🎫 Your Ticket")

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Booking ID:** {booking['booking_id']}"
            )

            st.write(
                f"**Name:** {booking['name']}"
            )

            st.write(
                f"**Movie:** {booking['movie']}"
            )

            st.write(
                f"**Cinema:** {booking['cinema']}"
            )

            st.write(
                f"**Location:** {booking['city']}"
            )

        with col2:

            st.write(
                f"**Date:** {booking['date']}"
            )

            st.write(
                f"**Show:** {booking['show']}"
            )

            st.write(
                f"**Seats:** {', '.join(booking['seats'])}"
            )

            st.write(
                f"**Category:** {booking['seat_category']}"
            )

            st.write(
                f"**Amount Paid:** ₹{booking['total']}"
            )


        # -------------------------------------------------
        # FOOD
        # -------------------------------------------------

        if booking["food"]:

            st.subheader("🍿 Food Ordered")

            for food in booking["food"]:

                st.write(
                    f"• {food}"
                )


        # -------------------------------------------------
        # QR-LIKE BOOKING CODE
        # -------------------------------------------------

        st.subheader("🔐 Booking Code")

        st.code(
            booking["booking_id"]
        )


        # -------------------------------------------------
        # TEXT TO SPEECH
        # -------------------------------------------------

        st.subheader("🔊 Voice Confirmation")

        voice_text = (

            f"Hello {booking['name']}. "

            f"Your movie ticket booking is confirmed. "

            f"You have booked {booking['movie']} "

            f"at {booking['cinema']} "

            f"in {booking['city']}. "

            f"The show is on {booking['date']} "

            f"at {booking['show']}. "

            f"Your seats are "
            f"{', '.join(booking['seats'])}. "

            f"The total amount paid is "
            f"{booking['total']} rupees. "

            f"Your booking ID is "
            f"{booking['booking_id']}. "

            f"Thank you."
        )


        try:

            audio_file = "booking_confirmation.mp3"

            tts = gTTS(
                text=voice_text,
                lang="en"
            )

            tts.save(audio_file)

            st.audio(
                audio_file,
                format="audio/mp3"
            )

        except Exception as error:

            st.warning(
                f"Voice generation failed: {error}"
            )


# =========================================================
# BOOKING HISTORY
# =========================================================

with tab_history:

    st.header("📜 Booking History")

    if not st.session_state.bookings:

        st.info(
            "No bookings yet."
        )

    else:

        for booking in reversed(
            st.session_state.bookings
        ):

            with st.expander(
                f"🎬 {booking['movie']} — "
                f"{booking['date']} — "
                f"{booking['booking_id']}"
            ):

                st.write(
                    f"**Cinema:** {booking['cinema']}"
                )

                st.write(
                    f"**Show:** {booking['show']}"
                )

                st.write(
                    f"**Seats:** "
                    f"{', '.join(booking['seats'])}"
                )

                st.write(
                    f"**Amount:** ₹{booking['total']}"
                )

                st.write(
                    f"**Payment:** {booking['payment']}"
                )