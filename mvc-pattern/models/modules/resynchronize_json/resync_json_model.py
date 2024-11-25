import json
import os
from deepdiff import DeepDiff

# Model
class JsonResynchronizerModel:
    def __init__(self, server_json_path, local_json_path):
        self.server_json_path = server_json_path
        self.local_json_path = local_json_path

    def read_json_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file), None
        except Exception as e:
            return None, e

    def write_json_file(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, indent=4)
            return True, None
        except Exception as e:
            return False, e

    def compare_json(self):
        server_json, err = self.read_json_file(self.server_json_path)
        if err:
            return False, "Error fetching server JSON", err

        local_json, err = self.read_json_file(self.local_json_path)
        if err:
            return False, "Error reading local JSON", err

        if server_json != local_json:
            return True, "JSON data is NOT synchronized", None
        else:
            return False, "JSON data is resynchronized", None
        
    def get_json_difference_detailed(self):
        server_json, err = self.read_json_file(self.server_json_path)
        if err:
            print("Server JSON error:", err)
        
        local_json, err = self.read_json_file(self.local_json_path)
        if err:
            print("Local JSON error:", err)

        # Only proceed if both JSON objects are successfully retrieved
        if server_json is not None and local_json is not None:
            diff = DeepDiff(local_json, server_json, ignore_order=True).pretty()
            return diff if diff else "No differences found.", None
        else:
            return None, "Failed to load JSON data."

    def ensure_local_json(self):
        """
        Ensure the local JSON file exists.
        If it does not, copy the server JSON file to the local path.
        """
        # Check if the local JSON file exists
        if not os.path.isfile(self.local_json_path):
            try:
                # Read the server JSON
                server_json, err = self.read_json_file(self.server_json_path)
                if err:
                    return False, "Error fetching server JSON", err

                # Write the server JSON to the local path
                success, write_err = self.write_json_file(self.local_json_path, server_json)
                if not success:
                    return False, "Failed to write server JSON to local path", write_err
                
                return True, "Server JSON copied to local path", None
            except Exception as e:
                return False, "Unexpected error", e
        return True, "Local JSON exists", None