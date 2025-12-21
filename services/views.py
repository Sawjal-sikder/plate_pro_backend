from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from .serializers import PlateDataSerializer
from .utils import calculate_area, generate_dxf


class PlateCalculationView(APIView):
    """
    API endpoint to calculate area and generate AutoCAD DXF file from plate data.
    
    POST /api/services/calculate/
    """
    
    def post(self, request):
        """
        Accept plate data JSON and return calculated area and AutoCAD file info.
        """
        serializer = PlateDataSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "message": "Invalid data format",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        corners = validated_data['corners']
        holes = validated_data.get('holes', [])
        
        try:
            # Calculate area
            area_data = calculate_area(corners, holes)
            
            # Generate DXF file
            dxf_buffer = generate_dxf(corners, holes)
            dxf_content = dxf_buffer.read()
            
            # Encode DXF content to base64 for JSON response
            import base64
            dxf_base64 = base64.b64encode(dxf_content).decode('utf-8')
            
            return Response({
                "status": "success",
                "data": {
                    "area_calculations": area_data,
                    "autocad": {
                        "dxf_file_base64": dxf_base64,
                        "filename": "shape.dxf",
                        "message": "DXF file generated successfully",
                        "download_instructions": "Decode the base64 string to get the DXF file"
                    },
                    "input_summary": {
                        "total_corners": len(corners),
                        "total_holes": len(holes),
                        "view_box": validated_data['viewBox'],
                        "color": validated_data['color']
                    }
                }
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error processing data: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DownloadDXFView(APIView):
    """
    API endpoint to directly download the DXF file.
    
    POST /api/services/download-dxf/
    """
    
    def post(self, request):
        """
        Accept plate data JSON and return DXF file as downloadable attachment.
        """
        serializer = PlateDataSerializer(data=request.data)
        
        if not serializer.is_valid():
            return Response({
                "status": "error",
                "message": "Invalid data format",
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)
        
        validated_data = serializer.validated_data
        corners = validated_data['corners']
        holes = validated_data.get('holes', [])
        
        try:
            # Generate DXF file
            dxf_buffer = generate_dxf(corners, holes)
            
            # Return as downloadable file
            response = HttpResponse(
                dxf_buffer.read(),
                content_type='application/dxf'
            )
            response['Content-Disposition'] = 'attachment; filename="plate_shape.dxf"'
            
            return response
            
        except Exception as e:
            return Response({
                "status": "error",
                "message": f"Error generating DXF file: {str(e)}"
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
