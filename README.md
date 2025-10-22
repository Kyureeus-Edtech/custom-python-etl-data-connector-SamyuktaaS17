# ip-api.com Custom ETL Connector

This project connects to three endpoints from ip-api.com, extracts geolocation/IP data, transforms the output for MongoDB compatibility, and loads it into the database.

## API Endpoints Used
- `/json/{query}` : Single IP lookup, returns JSON
- `/batch` : Batch IP lookup, POST a list of IPs, returns JSON
- `/csv/{query}` : Single IP lookup, returns CSV string

## Usage

1. Clone the repo and create a new branch.
2. Create a `.env` file with your MongoDB URI:
    ```
    MONGO_URI=mongodb://localhost:27017/
    ```
3. Install dependencies:
    ```
    pip install -r requirements.txt
    ```
4. Run ETL script:
    ```
    python etl_connector.py
    ```

## Example Output

MongoDB documents contain:
- All API response fields
- Endpoint used
- Query IP
- `ingested_at` timestamp

## Project Structure
/samyuktaa_121_A2/
├── etl_connector.py
├── requirements.txt
├── README.md
