# Plate Pro API

## Overview

Plate Pro is a comprehensive plate manufacturing and processing platform that provides custom plate shape design, drilling services, area calculations, and DXF file generation for CNC machining. The API enables applications to create custom plate designs with precise geometric specifications, calculate manufacturing costs, and generate technical drawings for production.

## Authentication

Most endpoints require Bearer token authentication:

```
Authorization: Bearer {access_token}
```

Obtain tokens through the login endpoint using email and password credentials.

## Base URL

Configure the BASE_URL environment variable in your Postman environment.

## Core Features

### 1. Authentication & User Management

- **Email/Password Registration**: User signup with email verification
- **Login**: JWT-based authentication with access and refresh tokens
- **Password Recovery**: Forgot password with email verification codes
- **Profile Management**: Update user information and profile images
- **User Administration**: List all users, view user details, activate/deactivate accounts
- **Premium Status**: Manage user premium permissions
- **Social Authentication**: Google login integration

### 2. Plate Shape Management

Create and manage custom plate shapes with precise geometric specifications:

**Plate Shape Features:**

- **Coordinate-Based Design**: Define shapes using X,Y coordinate points
- **Custom Icons**: Upload visual representations of plate shapes
- **Closed/Open Shapes**: Support for both closed polygons and open polylines
- **Active Status**: Enable/disable specific plate shapes
- **CRUD Operations**: Create, read, update, and delete plate shapes

**Plate Shape Object:**

```json
{
  "id": 1,
  "name": "Rectangular Plate",
  "icon": "url_to_icon",
  "description": "Standard rectangular steel plate",
  "points": [
    [0, 0],
    [100, 0],
    [100, 50],
    [0, 50]
  ],
  "closed": true,
  "is_active": true,
  "created_at": "2026-01-12T10:00:00Z",
  "updated_at": "2026-01-12T10:00:00Z"
}
```

### 3. Plate Variants & Pricing

Manage different variants of plate shapes with specific pricing:

**Plate Variant Features:**

- Associated with plate shapes
- Individual pricing per variant
- Material type specifications
- Thickness options
- Custom naming conventions

**Plate Variant Object:**

```json
{
  "id": 1,
  "plate_shape": 1,
  "name": "1/4 inch Steel Plate",
  "price": 25.99,
  "is_active": true,
  "created_at": "2026-01-12T10:00:00Z",
  "updated_at": "2026-01-12T10:00:00Z"
}
```

### 4. Drilling Services

Manage hole drilling services for plates:

**Drilling Service Features:**

- Price per hole calculations
- Various hole sizes and types
- Custom drilling patterns
- Service availability management

**Drilling Service Object:**

```json
{
  "id": 1,
  "name": "Standard 1/4 inch Holes",
  "price_per_hole": 2.5,
  "is_active": true,
  "created_at": "2026-01-12T10:00:00Z",
  "updated_at": "2026-01-12T10:00:00Z"
}
```

### 5. Plate Calculation & DXF Generation

Advanced calculation engine for plate manufacturing:

**Calculation Features:**

- **Area Calculation**: Precise area calculations for complex shapes
- **Hole Compensation**: Account for drilled holes in area calculations
- **DXF Generation**: Generate AutoCAD-compatible files for CNC machining
- **Cost Estimation**: Real-time pricing calculations

**Calculation Request:**

```json
{
  "corners": [
    [0, 0],
    [100, 0],
    [100, 50],
    [0, 50]
  ],
  "holes": [
    {
      "center": [25, 25],
      "radius": 5
    },
    {
      "center": [75, 25],
      "radius": 5
    }
  ]
}
```

**Calculation Response:**

```json
{
  "status": "success",
  "data": {
    "area_calculations": {
      "total_area": 5000.0,
      "hole_area": 157.08,
      "net_area": 4842.92,
      "perimeter": 300.0
    },
    "autocad": {
      "download_url": "/media/dxf/plate_shape_a1b2c3d4.dxf",
      "filename": "plate_shape_a1b2c3d4.dxf"
    }
  }
}
```

### 6. Shopping Cart Management

Complete cart functionality for ordering plates and services:

**Cart Features:**

- Add plate variants to cart
- Add drilling services with hole counts
- Quantity management
- Automatic total price calculation
- Item type validation

**Cart Item Object:**

```json
{
  "id": 1,
  "item_type": "variant",
  "plate_variant": 1,
  "quantity": 2,
  "drilling_service": null,
  "holes_count": null,
  "total_price": 51.98,
  "created_at": "2026-01-12T10:00:00Z",
  "updated_at": "2026-01-12T10:00:00Z"
}
```

## API Endpoints

### Authentication Endpoints

- `POST /api/accounts/auth/register/` - User registration
- `POST /api/accounts/auth/login/` - User login
- `POST /api/accounts/auth/refresh/` - Refresh access token
- `POST /api/accounts/auth/logout/` - User logout
- `POST /api/accounts/auth/forgot-password/` - Request password reset
- `POST /api/accounts/auth/verify_code/` - Verify reset code
- `POST /api/accounts/auth/set_new_password/` - Set new password
- `POST /api/accounts/auth/change-password/` - Change password
- `GET /api/accounts/auth/user/details/` - Get current user details
- `PATCH /api/accounts/auth/users/update/` - Update user profile

### Admin User Management

- `GET /api/accounts/auth/users/` - List all users (Admin only)
- `GET /api/accounts/auth/users/{id}/` - Get user details (Admin only)
- `POST /api/accounts/auth/users/activate/{id}/` - Activate/deactivate user
- `POST /api/accounts/auth/users/premium/{id}/` - Set premium status

### Plate Shape Endpoints

- `GET /api/services/plate-shapes/list/` - List active plate shapes
- `GET /api/services/plate-shapes/details/{id}/` - Get plate shape details
- `GET /api/services/plate-shapes/` - List all plate shapes (Admin)
- `POST /api/services/plate-shapes/` - Create new plate shape (Admin)
- `GET /api/services/plate-shapes/{id}/` - Get plate shape (Admin)
- `PUT /api/services/plate-shapes/{id}/` - Update plate shape (Admin)
- `DELETE /api/services/plate-shapes/{id}/` - Delete plate shape (Admin)

### Plate Variant Endpoints

- `GET /api/services/plate-variants/` - List plate variants
- `POST /api/services/plate-variants/` - Create plate variant (Admin)
- `GET /api/services/plate-variants/{id}/` - Get plate variant details
- `PUT /api/services/plate-variants/{id}/` - Update plate variant (Admin)
- `DELETE /api/services/plate-variants/{id}/` - Delete plate variant (Admin)

### Drilling Service Endpoints

- `GET /api/services/drilling-services/` - List drilling services
- `POST /api/services/drilling-services/` - Create drilling service (Admin)
- `GET /api/services/drilling-services/{id}/` - Get drilling service details
- `PUT /api/services/drilling-services/{id}/` - Update drilling service (Admin)
- `DELETE /api/services/drilling-services/{id}/` - Delete drilling service (Admin)

### Calculation & DXF Generation

- `POST /api/services/calculate/` - Calculate plate area and generate DXF

### Cart Management

- `GET /api/services/cart-items/` - List user's cart items
- `POST /api/services/cart-items/` - Add item to cart
- `PUT /api/services/cart-items/{id}/` - Update cart item
- `DELETE /api/services/cart-items/{id}/` - Remove item from cart

## Data Structures

### User Registration

```json
{
  "email": "user@example.com",
  "full_name": "John Doe",
  "phone_number": "1234567890",
  "password": "securepassword",
  "password2": "securepassword"
}
```

### User Profile Update

```json
{
  "full_name": "John Doe",
  "email": "user@example.com",
  "phone_number": "1234567890",
  "profile_image": "file"
}
```

### Plate Shape Creation

```json
{
  "name": "Custom L-Shape",
  "description": "L-shaped steel plate for corner applications",
  "points": [
    [0, 0],
    [100, 0],
    [100, 30],
    [30, 30],
    [30, 100],
    [0, 100]
  ],
  "closed": true,
  "icon": "file",
  "is_active": true
}
```

### Cart Item Addition

```json
{
  "item_type": "variant",
  "plate_variant": 1,
  "quantity": 3
}
```

```json
{
  "item_type": "drilling",
  "drilling_service": 1,
  "holes_count": 8
}
```

## Environment Variables

Set these in your environment:

- `BASE_URL`: API server base URL
- `SECRET_KEY`: Django secret key
- `DEBUG`: Debug mode (True/False)
- `DATABASE_URL`: Database connection string
- `REDIS_URL`: Redis connection for Celery
- `EMAIL_HOST`: SMTP server for email
- `EMAIL_HOST_USER`: Email username
- `EMAIL_HOST_PASSWORD`: Email password
- `GOOGLE_OAUTH2_KEY`: Google OAuth client ID
- `GOOGLE_OAUTH2_SECRET`: Google OAuth client secret

## Response Formats

All responses are in JSON format:

- **Success**: Relevant data with 200/201 status codes
- **Error**: Error messages with appropriate status codes
- **Timestamps**: ISO 8601 format where applicable

## Status Codes

- `200 OK`: Successful GET/PATCH/PUT request
- `201 Created`: Successful POST request
- `204 No Content`: Successful DELETE request
- `400 Bad Request`: Invalid parameters or missing required fields
- `401 Unauthorized`: Authentication required or invalid token
- `403 Forbidden`: Insufficient permissions
- `404 Not Found`: Resource not found
- `500 Internal Server Error`: Server error

## API Workflows

### Plate Design Workflow

1. Create custom plate shape with coordinate points
2. Set up plate variants with materials and pricing
3. Calculate area and generate DXF files
4. Add plate variants to shopping cart
5. Apply drilling services if needed
6. Process order

### Manufacturing Workflow

1. Design plate using coordinate system
2. Calculate material requirements and costs
3. Generate DXF file for CNC machining
4. Export technical drawings
5. Process manufacturing order

### User Management Workflow

1. User registers with email verification
2. Admin reviews and activates account
3. User logs in and receives JWT tokens
4. User designs plates and calculates costs
5. User adds items to cart and places orders
6. Admin manages users and premium features

## Plate Design Use Cases

### Custom Manufacturing

- Design complex plate shapes for specific applications
- Calculate exact material requirements
- Generate precision DXF files for CNC cutting
- Cost estimation for manufacturing quotes

### Steel Fabrication

- Create templates for common plate shapes
- Standard hole drilling patterns
- Material optimization calculations
- Production planning and costing

### Engineering Applications

- Structural steel plate design
- Custom brackets and mounting plates
- Architectural metalwork
- Industrial equipment components

### Educational Use

- CAD/CAM training programs
- Manufacturing process education
- Geometric calculation examples
- Technical drawing generation

## Best Practices

### Plate Design

- **Coordinate Precision**: Use precise coordinate values for accurate manufacturing
- **Shape Validation**: Ensure closed shapes for area calculations
- **Point Order**: Define points in clockwise or counter-clockwise order consistently
- **Material Consideration**: Account for material thickness in hole placement

### API Usage

- **Authentication**: Always include valid JWT tokens
- **Input Validation**: Validate coordinate data before submission
- **Error Handling**: Implement proper error handling for failed calculations
- **File Management**: Handle DXF file downloads appropriately

### Performance

- **Calculation Optimization**: Cache complex area calculations when possible
- **File Storage**: Implement proper cleanup for generated DXF files
- **Database Queries**: Use efficient queries for large plate catalogs
- **Image Optimization**: Compress plate shape icons before upload

## Getting Started

1. **Set up environment variables**
2. **Register user account with email**
3. **Admin activates account**
4. **Login to obtain access token**
5. **Browse available plate shapes**
6. **Create custom designs or use templates**
7. **Calculate areas and costs**
8. **Generate DXF files for manufacturing**
9. **Add items to cart and place orders**

## Security Considerations

- **JWT Authentication**: Secure API access with JWT tokens
- **Email Verification**: Required for user registration
- **Admin Approval**: Admin activation required for new accounts
- **Input Validation**: Validate all coordinate and numerical inputs
- **File Security**: Secure handling of uploaded images and generated DXF files
- **Access Control**: Implement proper authorization checks

## Admin Features

Admin users have access to:

- **User Management**: Activate/deactivate users and set premium status
- **Plate Shape Management**: Create, update, and delete plate shapes
- **Variant Management**: Manage pricing and availability
- **Service Management**: Configure drilling services and pricing
- **System Monitoring**: View user activity and system metrics

## Technical Specifications

### Coordinate System

- **Units**: All coordinates in millimeters or inches (configurable)
- **Origin**: (0,0) at bottom-left corner
- **Precision**: Up to 3 decimal places for manufacturing accuracy

### DXF File Generation

- **Format**: AutoCAD DXF R14 compatible
- **Layers**: Separate layers for plate outline and holes
- **Units**: Metric (mm) or Imperial (inches)
- **Compatibility**: Works with major CAD/CAM software

### Calculation Engine

- **Area Algorithm**: Surveyor's formula for polygon area calculation
- **Hole Compensation**: Precise circular area subtraction
- **Validation**: Input validation for geometric consistency

## Docker Support

The application includes full Docker support:

```bash
# Build and run with Docker Compose
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## Celery Task Processing

Background task processing for:

- Email sending for user verification
- Large file processing and DXF generation
- Bulk calculations and exports
- Scheduled cleanup tasks

## Support

For API support, integration questions, or feature requests, contact the development team.

## Version Information

- **API Version**: 1.0
- **Django Version**: 4.x
- **DRF Version**: 3.x
- **Database**: PostgreSQL (recommended) / SQLite (development)
- **Cache**: Redis
- **Task Queue**: Celery with Redis broker
