from pymongo import MongoClient, errors, ReturnDocument
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
import logging
import os
from dotenv import load_dotenv

# Configuración del registro de errores
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
load_dotenv()
class DatabaseConnection:
    """
    DatabaseConnection es una clase que maneja la conexión a una base de datos MongoDB y proporciona métodos para realizar operaciones CRUD (Crear, Leer, Actualizar, Eliminar) en las colecciones de la base de datos.
    Métodos de Clase:
    - connect(cls): Establece la conexión a la base de datos.
    - get_collection(cls, collection_name): Obtiene una colección específica de la base de datos.
    - create_document(cls, collection_name, document): Crea un nuevo documento en la colección especificada.
    - read_document(cls, collection_name, document_id): Lee un documento por su ID.
    - update_document(cls, collection_name, document_id, updated_fields): Actualiza un documento existente con los campos proporcionados.
    - delete_document(cls, collection_name, document_id): Elimina un documento por su ID.
    - close_connection(cls): Cierra la conexión a la base de datos.
    Atributos de Clase:
    - _client: Instancia del cliente MongoDB.
    - _db: Instancia de la base de datos MongoDB.
    Excepciones:
    - errors.ConnectionError: Se lanza si hay un error al establecer la conexión a la base de datos.
    - errors.PyMongoError: Se lanza si hay un error al realizar operaciones CRUD.
    - errors.InvalidId: Se lanza si el ID del documento no es válido.
    """
    # Variable de clase para la instancia del cliente
    _client = None
    _db = None

    @classmethod
    def connect(cls):
        """
        Establish a connection to the database.

        This method initializes a MongoDB client using the provided URI and
        certificate key file. If the connection is successful, it sets the
        client and database attributes for the class. If the connection fails,
        it logs an error message and raises a ConnectionError.

        Raises:
            errors.ConnectionError: If there is an error connecting to the database.
        """
        """Establecer la conexión a la base de datos."""
        if cls._client is None:
            try:
                uri = f"mongodb+srv://{os.getenv('USER')}:{os.getenv('PASSWD')}@omrcluster.p3thf.mongodb.net/?retryWrites=true&w=majority&appName=OMRcluster"                
                cls._client = MongoClient(uri, server_api=ServerApi('1'))
                cls._db = cls._client['omrdb']
                logger.info("Conexión establecida a la base de datos.")
            except errors.ConnectionFailure as e:
                logger.error(f"Error de conexión a la base de datos: {e}")
                raise

    @classmethod
    def get_collection(cls, collection_name):
        """Obtener una colección específica de la base de datos."""
        cls.connect()  # Asegurarse de que la conexión esté activa
        return cls._db[collection_name]
    
    @classmethod
    def count_documents(cls, collection_name, query):
        collection = cls.get_collection(collection_name)
        return float(collection.count_documents(query))
    
    @classmethod
    def create_document(cls, collection_name, document):
        """Crear un nuevo documento en la colección."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.insert_one(document)
            document['_id'] = result.inserted_id.binary.hex() 

            logger.info(f"Documento creado con ID: {result.inserted_id}")
            return document
        except errors.PyMongoError as e:
            logger.error(f"Error al crear el documento: {e}")
            raise

    @classmethod
    def read_document(cls, collection_name, document_id : str, projection = None, sort_criteria = None):
        """Leer un documento por su ID."""
        collection = cls.get_collection(collection_name)
        try:
            document = collection.find_one({"_id": ObjectId(document_id)}, projection)
            
            if document is None:
                logger.warning(f"Documento con ID {document_id} no encontrado.")
            else:
                document['_id'] = document_id
            
            if sort_criteria:
                documents = documents.sort(sort_criteria)
            
            return document
        except errors.InvalidId as e:
            logger.error(f"ID de documento no válido: {e}")
            raise
    
    @classmethod
    def query_document(cls, collection_name, document_query, projection = None, sort_criteria = None, skip = 0, limit = 0):
        """Realizar query según los parámetros."""
        collection = cls.get_collection(collection_name)
        try:
            documents = collection.find(document_query, projection)
 
            if limit > 0:
                documents.limit(limit)
            if skip > 0:
                documents.skip(skip)
            if sort_criteria:
                documents.sort(sort_criteria)

            if not documents:
                logger.warning(f"No se encontraron documentos con la consulta: {document_query}")

            return documents
        except Exception as e:
            logger.error(f"Error al realizar la consulta: {e}")
            raise


    @classmethod
    def update_document(cls, collection_name, document_id, updated_fields, original_id):
        """Actualizar un documento existente y devolver el documento actualizado."""
        collection = cls.get_collection(collection_name)
        try:
            original_document = collection.find_one({"_id": ObjectId(document_id)})
            if original_document is None:
                logger.warning(f"No se encontró el documento con ID {document_id} para copiar.")
                return None

            new_document = original_document.copy()
            new_document['_id'] = ObjectId()
            new_document.update(updated_fields)
            collection.insert_one(new_document)

            new_document['_id'] = new_document['_id'].binary.hex()         

            logger.info(f"Documento con ID {document_id} copiado y actualizado a nuevo documento con ID {new_document['_id']}.")
            return new_document

        except errors.PyMongoError as e:
            logger.error(f"Error al actualizar el documento: {e}")
            raise
    
    @classmethod
    def update_document_real(cls, collection_name, document_id, updated_fields):
        """Actualizar un documento existente y devolver el documento actualizado."""
        collection = cls.get_collection(collection_name)
        try:
            updated_document = collection.find_one_and_update(
                {"_id": ObjectId(document_id)},
                {"$set": updated_fields},
                return_document=True 
            )

            if updated_document is None:
                logger.warning(f"No se encontró el documento con ID {document_id} para actualizar.")
            else:
                updated_document['_id'] = updated_document['_id'].binary.hex()

                logger.info(f"Documento con ID {document_id} actualizado.")

            return updated_document

        except errors.PyMongoError as e:
            logger.error(f"Error al actualizar el documento: {e}")
            raise


    @classmethod
    def delete_document(cls, collection_name, document_id):
        """Eliminar un documento por su ID."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.delete_one({"_id": ObjectId(document_id)})
            if result.deleted_count == 0:
                logger.warning(f"No se encontró el documento con ID {document_id} para eliminar.")
            else:
                logger.info(f"Documento con ID {document_id} eliminado.")
            return result.deleted_count
        except errors.InvalidId as e:
            logger.error(f"ID de documento no válido: {e}")
            raise

    @classmethod
    def delete_multiple_documents(cls, collection_name, query):
        """Eliminar múltiples documentos según un query."""
        collection = cls.get_collection(collection_name)
        try:
            result = collection.delete_many(query)
            if result.deleted_count == 0:
                logger.warning(f"No se encontraron documentos que coincidan con el query {query} para eliminar.")
            else:
                logger.info(f"Se eliminaron {result.deleted_count} documentos que coinciden con el query.")
            return result.deleted_count
        except errors.PyMongoError as e:
            logger.error(f"Error al intentar eliminar documentos: {e}")
            raise

    @classmethod
    def close_connection(cls):
        """Cerrar la conexión a la base de datos."""
        if cls._client is not None:
            cls._client.close()
            cls._client = None
            cls._db = None
            logger.info("Conexión a la base de datos cerrada.")