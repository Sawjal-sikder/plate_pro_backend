from ..utils import calculate_area, generate_dxf
from rest_framework.response import Response
from ..serializers.serializers import PlateDataSerializer
from rest_framework.views import APIView
from django.http import HttpResponse
from rest_framework import status
from django.conf import settings
import uuid
import os


class PlateCalculationView(APIView):

    def post(self, request):       
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
            area_data = calculate_area(corners, holes)
          
            dxf_buffer = generate_dxf(corners, holes)
            
            dxf_dir = os.path.join(settings.MEDIA_ROOT, 'dxf')
            os.makedirs(dxf_dir, exist_ok=True)
            
            filename = f"plate_shape_{uuid.uuid4().hex[:8]}.dxf"
            file_path = os.path.join(dxf_dir, filename)
            
            # Save to filesystem
            with open(file_path, 'wb') as f:
                f.write(dxf_buffer.getvalue())
            
            # Generate download URL
            download_url = f"{settings.MEDIA_URL}dxf/{filename}"
            
            return Response({
                "status": "success",
                "data": {
                    "area_calculations": area_data,
                    "autocad": {
                        "download_url": request.build_absolute_uri(download_url),
                        # "filename": filename,
                        # "message": "DXF file generated successfully"
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
