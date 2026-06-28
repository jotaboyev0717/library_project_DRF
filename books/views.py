from django.db.models import query
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Book
from .serializers import BookSerializer
from rest_framework import viewsets
from rest_framework.viewsets import ModelViewSet
# Create your views here.

# class BookListApiView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookListApiView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many = True)
        data = {
            "status": f"Returned {len(books)} books",
            "data": serializer.data
        }
        return Response(data)

# class BookDetailApiView(generics.RetrieveAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookDetailApiView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            serializer = BookSerializer(book).data
            data = {
                "status": "success",
                "data": serializer
            }
            return Response(data)
        except Book.DoesNotExist:
            return Response({
                "status": "error",
                "message": "Book not found"
            }, status=status.HTTP_404_NOT_FOUND)
    
# class BookDeleteApiView(generics.DestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookDeleteApiView(APIView):
    def delete(self, request, pk):
        try:
            book = Book.objects.get(pk=pk)
            book.delete()
            data = {
                "status": "success",
                "message": "Book deleted successfully"
            }
            return Response(data)
        except Exception:
            return Response({
                "status": "False",
                "message": "Book not found"
            }, status=status.HTTP_404_NOT_FOUND)

# class BookUpdateApiView(generics.UpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookViewset(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateApiView(APIView):
    def put(self, request, pk):
        book = get_object_or_404(Book, pk=pk)
        data = request.data
        serializer = BookSerializer(book, data=data, partial =True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({
                "status":"True",
                "message":"Book updated successfully",
            }) 



# class BookCreateApiView(generics.CreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializer

class BookCreateApiView(APIView):
    def post(self, request):
        data = request.data
        serializer = BookSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response({
            "status": "success",
            "data": serializer.data
        })

class BookListCreateApiView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

@api_view(["GET"])
def books_list_view(request, *args, **kwargs):
    books = Book.objects.all()
    serializer = BookSerializer(books, many = True)
    return Response(serializer.data)
        
