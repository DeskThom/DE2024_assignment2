import random
import json
import pandas as pd
from datetime import datetime, timedelta

def outage_simulator(num_rows: int) -> pd.DataFrame:
    # Expanded list of diverse cities in the Netherlands
    cities = [
        "Amsterdam", "Rotterdam", "The Hague", "Utrecht", "Eindhoven", 
        "Tilburg", "Groningen", "Almere", "Breda", "Nijmegen", 
        "Apeldoorn", "Haarlem", "Arnhem", "Amersfoort", "Maastricht",
        "Delft", "Leiden", "Zwolle", "Den Bosch", "Enschede",
        "Leeuwarden", "Middelburg", "Hoorn", "Helmond", "Roermond",
        "Assen", "Deventer", "Oss", "Gouda", "Veenendaal",
        "Hengelo", "Zaandam", "Zoetermeer", "Lelystad", "Alkmaar",
        "Zaanstad", "Hoofddorp", "Ede", "Venlo", "Haarlemmermeer",
        "Emmen", "Sittard", "Weert", "Tiel", "Harderwijk",
        "Barneveld", "Hellevoetsluis", "Purmerend", "Gorinchem", "Vlaardingen",
        "Spijkenisse", "Capelle aan den IJssel", "Rijswijk", "Katwijk", "Dronten",
        "Wageningen", "Nieuwegein", "Zeist", "Culemborg", "Meppel",
        "Doetinchem", "Heerlen", "Ridderkerk", "Zutphen", "Schiedam",
        "Hoogeveen", "Oosterhout", "Dongen", "IJsselstein", "Baarn",
        "Hilversum", "Bunschoten", "Bergen op Zoom", "Veghel", "Boxmeer",
        "Landgraaf", "Kerkrade", "Voorschoten", "Pijnacker", "Staphorst",
        "Alblasserdam", "Oegstgeest", "Heerenveen", "Etten-Leur", "Zwijndrecht"
    ]

    # Function to generate a random date within the last 30 days
    def random_date():
        start_date = datetime.now() - timedelta(days=30)
        random_days = random.randint(0, 30)
        return (start_date + timedelta(days=random_days)).strftime('%d-%m-%Y')

    # Function to generate a random time
    def random_time():
        return f"{random.randint(0, 23):02}:{random.randint(0, 59):02}"

    # Generate unique rows of data
    unique_data = set()
    while len(unique_data) < num_rows:
        row = (
            random_date(),
            random_time(),
            random.choice(cities),
        )
        unique_data.add(row)  # Add row only if it's not already in the set

    # Convert to a DataFrame
    data = [{"date": r[0], "time": r[1], "city": r[2]} for r in unique_data]
    
    df = pd.DataFrame(data)
    
    # Sort by date and time to ensure the data is ordered from oldest to newest
    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%d-%m-%Y %H:%M')
    df = df.sort_values(by='datetime')

    df['datetime'] = df['datetime'].dt.strftime('%Y-%m-%d %H:%M:%S')

    df = df.drop(columns=["date","time"])
    
    return df

# Generate data and save to CSV with timestamped filename
def save_data_to_csv(df: pd.DataFrame):
    """
    Saves a dataframe to a csv file with a timestamp
    """
    # Get the current timestamp for the filename
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    
    # Generate the filename
    filename = f"outage_data_{timestamp}.csv"
    
    # Save the DataFrame to CSV
    df.to_csv(filename, index=False)
    print(f"Data saved to {filename}")


# Function to save the generated data as a JSON file
def save_data_to_json(filename: str, num_records: int):
    """
    Saves the simulated data to a JSON file
    """
    data = outage_simulator(num_records)
    
    data = data.to_dict(orient='records')
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"outage_data_{timestamp}.json" 
    
    with open(filename, 'w') as f:
        for record in data:
            f.write(json.dumps(record, separators=(',', ':')) + '\n')

# Generate 10,000 rows of unique data
outage_data = outage_simulator(10000)

# Save to CSV with a timestamped filename
save_data_to_json(outage_data, 10000)
