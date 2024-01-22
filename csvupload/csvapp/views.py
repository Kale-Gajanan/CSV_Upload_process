#from datetime import timezone
import uuid

import pymongo
from bson import ObjectId  # Import ObjectId from bson module
from django.utils import timezone
from django.shortcuts import render
from .utils import connect_to_mongodb,fetch_data_from_mongodb
import pandas as pd
from pymongo.errors import DuplicateKeyError
# Create your views here.
# csvapp/views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import UploadedFile
from .forms import UploadedFileForm  # Create a form for file uploads

def file_list(request):
    files = UploadedFile.objects.all()
    return render(request, 'file_list.html', {'files': files})

def file_detail(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    return render(request, 'file_detail.html', {'file': file})

def file_upload(request):
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = UploadedFileForm()
    return render(request, 'file_upload.html', {'form': form})

def file_edit(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    if request.method == 'POST':
        form = UploadedFileForm(request.POST, request.FILES, instance=file)
        if form.is_valid():
            form.save()
            return redirect('file_list')
    else:
        form = UploadedFileForm(instance=file)
    return render(request, 'file_edit.html', {'form': form})

def file_delete(request, pk):
    file = get_object_or_404(UploadedFile, pk=pk)
    if request.method == 'POST':
        file.delete()
        return redirect('file_list')
    return render(request, 'file_delete.html', {'file': file})


# csvapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import UploadedFile
from .forms import UploadedFileForm
import pandas as pd
from pymongo import MongoClient
from django.conf import settings
"""
def process_selected_files(request):
    global pd
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files')

        # Perform processing for the selected files
        for file_id in selected_files:
            file = get_object_or_404(UploadedFile, pk=file_id)

            # Read data from the selected file into a DataFrame
            df = pd.read_csv(file.filename.path, low_memory=False)  # Assuming CSV format, adjust if needed

            # Perform your processing logic here (e.g., modifying DataFrame)
            import pandas as pd
            import uuid

            # Assuming df is your DataFrame
            df['UniqueID'] = [str(uuid.uuid4()) for _ in range(len(df))]

            # Display the DataFrame with the new UniqueID column
            print(df[['Year', 'UniqueID']])  # Adjust the columns as needed
            # Replace None values with a valid value (e.g., 'unknown')
            print(df.columns)
            #df['your_unique_field'].fillna('unknown', inplace=True)

            # Bulk write the data to MongoDB
            bulk_write_mongodb1(df)

            # Update existing records in the UploadedFile model
            update_existing_records(file, df)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def bulk_write_mongodb(df):
    # Connect to MongoDB
    database_name = "road"
    collection_name = "rdata"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)

    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')

    # Bulk write to MongoDB
    collection.insert_many(data)

def update_existing_records(file, df):
    # Your logic to update existing records in the UploadedFile model
    # For example, you might want to update the timestamp or other fields
    file.timestamp = timezone.now()  # Update timestamp to current time
    file.save()
# csvapp/views.py
from pymongo import MongoClient
from django.conf import settings

def bulk_write_mongodb1(df):
    # Connect to MongoDB
    database_name = "road"
    collection_name = "rdata1"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)

    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    print(data[0]['UniqueID'])
    print(data[1])
    # Print the DataFrame to inspect the data
    #print(data[0][['your_unique_field']])
    # Create a unique index on the field that you want to be unique
    #collection.create_index([("your_unique_field", 1)], unique=True)
    # Perform bulk write to MongoDB, handling duplicates
    bulk_upsert(collection, data, 'UniqueID')
    
    # Bulk write to MongoDB, handling duplicates
    for record in data:
        try:
            # Try to insert the record; if a duplicate key error occurs, handle it
            collection.insert_one(record)
        except DuplicateKeyError:
            # Handle the duplicate record (update, skip, or handle in any desired way)
            update_existing_record1(collection, record)
    

def update_existing_record1(collection, record):
    # Your logic to update the existing record based on a unique identifier
    # For example, you might use the _id field as a unique identifier
    unique_id = record['_id']
    collection.update_one({'_id': unique_id}, {'$set': record})


# csvapp/views.py
from django.shortcuts import render
from django.http import JsonResponse
from pymongo import MongoClient
from django.conf import settings


"""
# csvapp/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .models import UploadedFile
from .forms import UploadedFileForm
import pandas as pd
from pymongo import MongoClient
from django.conf import settings
from .utils import connect_to_mongodb
from pymongo.errors import DuplicateKeyError


# Example usage in process_selected_files function:

def process_selected_files(request):
    global pd
    if request.method == 'POST':
        selected_files = request.POST.getlist('selected_files')
        # Initialize an empty DataFrame to store the concatenated data
        df_merged = pd.DataFrame()

        # Perform processing for the selected files
        for file_id in selected_files:
            file = get_object_or_404(UploadedFile, pk=file_id)

            # Read data from the selected file into a DataFrame
            df_csv = pd.read_csv(file.filename.path, low_memory=False)
            print("dfcsv", df_csv)

            # Read data from MongoDB into a DataFrame
            df_mongo = fetch_data_from_mongodb()
            print("dfm", df_mongo)

            # Concatenate both DataFrames along rows
            df_merged = pd.concat([df_merged, df_csv, df_mongo], ignore_index=True)
            print("dup",df_merged[df_merged.duplicated()])
            # Drop duplicates from the concatenated DataFrame
            # Drop the '_id' column if it exists
            df_merged = df_merged.drop('_id', axis=1, errors='ignore')
            df_merged = df_merged.drop_duplicates(keep="first")

            print("dfmerg", df_merged.info())
            print(df_merged)

            # Bulk write the merged data to MongoDB
            bulk_write_mongodb(df_merged)

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})

def fetch_data_from_mongodb():
    # Connect to MongoDB
    database_name = "road"
    collection_name = "rdata1"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)

    # Fetch data from MongoDB into a DataFrame
    cursor = collection.find()
    df = pd.DataFrame(list(cursor))

    return df

def bulk_delete_all(collection):
    try:
        result = collection.delete_many({})
        print(f"{result.deleted_count} documents deleted from MongoDB.")
    except errors.BulkWriteError as bwe:
        # Handle bulk write errors
        print(f"Bulk write error: {bwe.details}")
def bulk_write_mongodb(df):
    # Connect to MongoDB
    database_name = "road"
    collection_name = "rdata1"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)
    # Delete all documents from MongoDB before inserting new data
    bulk_delete_all(collection)
    # Convert DataFrame to a list of dictionaries
    data = df.to_dict(orient='records')
    # Bulk write to MongoDB with upsert option to handle duplicates
    try:
        result = collection.insert_many(data,ordered=False)  # ordered=False allows continued processing after a duplicate key error
        #print(f"{len(result.inserted_ids)} records inserted in MongoDB.")
    except errors.BulkWriteError as bwe:
        # Handle bulk write errors
        #print(f"Bulk write error: {bwe.details}")
        pass

    # Bulk write to MongoDB
    #bulk_upsert(collection, data, '_id')  # Using bulk_upsert to handle duplicates

    #print(f"{len(data)} records inserted/modified in MongoDB.")
def clear_all_documents(request):
    # Connect to MongoDB
    database_name = "road"
    collection_name = "rdata1"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)
    try:
        # Delete all documents in the collection
        result = collection.delete_many({})
        deleted_count = result.deleted_count
        message = f"{deleted_count} documents deleted successfully."
        status = 'success'
    except Exception as e:
        message = f"Error: {str(e)}"
        status = 'error'

    return JsonResponse({'status': status, 'message': message})

from pymongo import MongoClient, errors
from django.conf import settings
from pymongo.operations import InsertOne, UpdateOne

def bulk_upsert(collection, data, unique_field):
    """
    try:
        bulk_requests = []

        if unique_field:
            # Create a list of update requests for each record with a unique field
            bulk_requests.extend([
                UpdateOne(
                    {unique_field: record[unique_field]},
                    {'$set': record},
                    upsert=True
                ) for record in data
            ])

        # Create a list of insert requests for each record without a unique field
        #bulk_requests.extend([InsertOne(record) for record in data if not unique_field])

        # Execute the bulk write
        result = collection.bulk_write(bulk_requests)

        print(f"{result.inserted_count} records inserted, {result.modified_count} records modified.")

    except errors.BulkWriteError as bwe:
        # Handle bulk write errors
        print(f"Bulk write error: {bwe.details}")
    """

    # Insert many records into MongoDB
    try:
        result = collection.insert_many(data,ordered=False)
        print(f"{len(result.inserted_ids)} records inserted in MongoDB.")
    except errors.BulkWriteError as bwe:
        # Handle bulk write errors
        print(f"Bulk write error: {bwe.details}")


    for record in data:
        # Define the filter to find a matching document based on a unique field
        filter_criteria = {'_id': record['_id']}  # Adjust the field as needed

        # Update data if a document with the same unique identifier exists
        update_data = {'$set': record}

        # Use upsert=True to insert a new document if no match is found
        collection.update_one(filter_criteria, update_data, upsert=True)

    print(f"{len(data)} records inserted/updated in MongoDB.")

from django.http import JsonResponse
from .utils import connect_to_mongodb

from django.shortcuts import render
from django.http import JsonResponse
from .utils import connect_to_mongodb

def get_data(request):
    database_name = "road"
    collection_name = "rdata1"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)

    # Fetch data from MongoDB into a list of dictionaries
    data = list(collection.find({}, {'_id': False}))  # Exclude '_id' field
    print(data)

    # Return the data as JSON for DataTables if the request expects JSON
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse(data, safe=False)

    # If it's a regular request, render the HTML template with the data
    return render(request, 'data_table.html', {'data': data})

from django.shortcuts import render


def data_table(request):
    database_name = "road"
    collection_name = "rdata1"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)

    # Fetch data from MongoDB into a DataFrame
    cursor = collection.find()
    data=list(cursor)
    print(data[0])
    return render(request, 'data_table1.html',{"data":data})


from django.shortcuts import render
from django.views import View
from django.http import JsonResponse
from pymongo import MongoClient

class DataTableView(View):
    def get(self, request, *args, **kwargs):
        database_name = "road"
        collection_name = "rdata1"

        # Connect to MongoDB
        collection = connect_to_mongodb(database_name, collection_name)

        # Fetch data from MongoDB into a DataFrame
        cursor = collection.find()
        data = list(cursor)
        print(data[0])

        # Convert ObjectId to string for JSON serialization
        for item in data:
            for key, value in item.items():
                if isinstance(value, ObjectId):
                    item[key] = str(value)

        # Specify the columns for ordering
        order_columns = [field for field in data[0].keys()] if data else []

        # Get DataTables parameters
        draw = int(request.GET.get('draw', 1))
        start = int(request.GET.get('start', 0))
        length = int(request.GET.get('length', 34554))
        order_column_index = int(request.GET.get('order[0][column]', 0))
        order_direction = request.GET.get('order[0][dir]', 'asc')

        # Sort the data based on the selected column and direction
        if order_columns and 0 <= order_column_index < len(order_columns):
            order_column = order_columns[order_column_index]
            data = sorted(data, key=lambda x: x[order_column], reverse=(order_direction == 'desc'))

        # Paginate the data
        data = data[start:start + length]

        # Prepare context data for rendering the template
        context = {
            'draw': draw,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'data': data,
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


from django.shortcuts import render
from django.views import View
from pymongo import MongoClient
from bson import ObjectId

class DataTableView(View):
    template_name = 'data_table_view.html'

    def get_context_data(self, **kwargs):
        database_name = "road"
        collection_name = "rdata1"

        # Connect to MongoDB
        collection = connect_to_mongodb(database_name, collection_name)

        # Fetch data from MongoDB into a DataFrame
        cursor = collection.find()
        data = list(cursor)
        print(data[0])

        # Convert ObjectId to string for JSON serialization
        for item in data:
            for key, value in item.items():
                if isinstance(value, ObjectId):
                    item[key] = str(value)

        # Specify the columns for ordering
        order_columns = [field for field in data[0].keys()] if data else []

        # Get DataTables parameters
        draw = int(self.request.GET.get('draw', 1))
        start = int(self.request.GET.get('start', 0))
        length = int(self.request.GET.get('length', 2000))
        order_column_index = int(self.request.GET.get('order[0][column]', 0))
        order_direction = self.request.GET.get('order[0][dir]', 'asc')

        # Sort the data based on the selected column and direction
        if order_columns and 0 <= order_column_index < len(order_columns):
            order_column = order_columns[order_column_index]
            data = sorted(data, key=lambda x: x[order_column], reverse=(order_direction == 'desc'))

        # Paginate the data
        data = data[start:start + length]

        # Prepare context data for rendering the template
        context = {
            'draw': draw,
            'recordsTotal': len(data),
            'recordsFiltered': len(data),
            'data': data,
        }

        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


from django.http import JsonResponse
from django.views.decorators.http import require_GET
import random
import string

def generate_dummy_data(num_records):
    dummy_data = []
    for _ in range(num_records):
        record = {
            "field1": ''.join(random.choices(string.ascii_letters, k=5)),
            "field2": random.randint(1, 100),
            # Add more fields as needed
        }
        dummy_data.append(record)
    return dummy_data

from django.http import JsonResponse
from bson import ObjectId
import json

from django.http import JsonResponse
from bson import ObjectId
import json

from django.http import JsonResponse
from bson import ObjectId
import json

@require_GET
def get_data_json(request):
    # DataTables parameters
    draw = int(request.GET.get('draw', 1))
    start = int(request.GET.get('start', 0))
    length = int(request.GET.get('length', 100))
    order_column_index = int(request.GET.get('order[0][column]', 0))
    order_direction = request.GET.get('order[0][dir]', 'asc')
    search_value = request.GET.get('search[value]', '')

    # Actual total number of records (replace with your total count logic)
    total_records = 34554

    database_name = "road"
    collection_name = "rdata1"

    # Connect to MongoDB
    collection = connect_to_mongodb(database_name, collection_name)

    # Define the sort column based on DataTables parameters
    order_columns = [field for field in collection.find_one().keys()]  # Use MongoDB document fields as order columns
    sort_column = order_columns[order_column_index]

    # Define the sort direction
    sort_direction = pymongo.ASCENDING if order_direction == 'asc' else pymongo.DESCENDING

    # Fetch data from MongoDB with sorting, searching, and pagination
    query = {}

    # Apply specific search conditions for the "Year" field
    if search_value and search_value.isdigit():
        query['Year'] = int(search_value)

    cursor = collection.find(query, {'_id': False}).sort(sort_column, sort_direction).skip(start).limit(length)
    data_list = list(cursor)

    # Convert NaN values to None for proper JSON serialization
    for item in data_list:
        for key, value in item.items():
            if value != value:  # Check for NaN
                item[key] = None

    # Remove extra spaces from keys
    cleaned_data_list = [{key.strip(): value for key, value in item.items()} for item in data_list]

    # Convert ObjectId to string for JSON serialization
    for item in cleaned_data_list:
        for key, value in item.items():
            if isinstance(value, ObjectId):
                item[key] = str(value)

    # Prepare the response data in the DataTables format
    response_data = {
        'draw': draw,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,  # Replace with the actual filtered count
        'data': cleaned_data_list,
    }

    # Convert to JSON and handle non-serializable values
    json_data = json.dumps(response_data, default=str)

    return JsonResponse(json.loads(json_data), safe=False)



def datatable_example(request):
    return render(request, 'datatable_ex.html')  # Replace 'your_template_name' with the actual template name


from django.http import JsonResponse
from django.views.decorators.http import require_GET
import random
import string

def generate_dummy_data1(num_records):
    dummy_data = []
    for _ in range(num_records):
        record = {
            "field1": ''.join(random.choices(string.ascii_letters, k=5)),
            "field2": random.randint(1, 100),
            # Add more fields as needed
        }
        dummy_data.append(record)
    return dummy_data

@require_GET
def get_data_json1(request):
    num_records = int(request.GET.get('length', 100)) # Default to 10 records if not specified

    data_list = generate_dummy_data1(num_records)
    total_records = 34554#place with the actual total number of records

    response_data = {
        'data': data_list,
        'recordsTotal': total_records,
        'recordsFiltered': total_records,
    }
    print(response_data['data'][0:1])
    return JsonResponse(response_data, safe=False)

def datatable_example1(request):
    return render(request, 'datatable_x.html')  # Replace 'your_template_name' with the actual template name
