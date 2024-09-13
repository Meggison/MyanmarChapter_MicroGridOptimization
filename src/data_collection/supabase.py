import requests
import os

key = os.getenv('SUPABASE_KEY')

def get_village_cluster_data(cluster_id: int):
    """Pulls village cluster data from Supabase.

    Args:
        cluster_id (int): id of the cluster

    Returns:
        dict: dictionary of data
    """
    url = f"https://cphmccauqoykywnynuhg.supabase.co/rest/v1/VILLAGE_CLUSTER?id=eq.{cluster_id}&select=Pop,NumPeoplePerHH,X_deg,Y_deg"

    headers = {
        "apiKey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
    }

    response = requests.request("GET", url, headers=headers)

    res = response.json()
    return res[0]