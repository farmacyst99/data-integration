# 📊 Data Integration and Validation Pipeline

This project fetches and integrates gas prices, consumer price index (CPI), and simulated sales data, validates the merged dataset, and sends an alert email if validation fails.

---

## 🚀 Execution Instructions

### 1. **Install Requirements**
Ensure required Python libraries are installed:

```bash
pip install pandas python-dotenv
```

### 2. **Environment Setup**
Create a `.env` file in your project directory with the following content:

```dotenv
FRED_API=your_fred_api_key
SENDER_EMAIL=your_email@gmail.com
RECEIVER_EMAIL=receiver_email@gmail.com
EMAIL_PASSWORD=your_email_password
```

### 3. **Run the Script**
You can run the script manually:

```bash
python main_commented.py
```

Or schedule it monthly using `cron`:

```bash
0 7 1 * * /usr/bin/python3 /path/to/main_commented.py >> /path/to/log.txt 2>&1
```

---

## 🧠 Overview of the Approach

1. **Data Fetching**:
   - Gas price data and CPI are fetched from FRED using API keys.
   - Simulated sales data is generated using an internal module.

2. **Preprocessing**:
   - CPI and sales data are matched by month.
   - Sales + CPI data are merged with weekly gas price data using ISO week numbers.

3. **Validation**:
   - Ensures all required columns are present.
   - Checks for nulls, duplicates, unexpected data types, and suspicious value spikes.

4. **Notification**:
   - If validation fails, an email is sent with all error messages.

5. **Output**:
   - Cleaned, validated dataset is saved as `data/final_data_1.csv`.

---

## 🔍 Assumptions Made

- Sales data is simulated and assumes a fixed schema.
- Gas and CPI data are available and up-to-date from the FRED API.
- The weekly merge via `week_num` is sufficient despite potential year overlaps.
- The threshold for suspicious spikes is ±50% per week.
- Emails are sent via Gmail's SMTP server (`smtp.gmail.com:587`), and the app password method is used for secure access.

---

## 📁 Output
The final merged and validated dataset is saved at:
```
data/final_data_1.csv
```

---

## 📬 Contact
For support or questions, feel free to raise an issue or email the maintainer.
