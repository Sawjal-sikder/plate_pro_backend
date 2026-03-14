import io
import os
from celery import shared_task #type: ignore
from django.conf import settings #type: ignore
from reportlab.pdfgen import canvas #type: ignore
from django.core.mail import EmailMessage #type: ignore
from reportlab.lib.pagesizes import letter #type: ignore
from reportlab.lib import colors #type: ignore
from reportlab.platypus import Table, TableStyle, SimpleDocTemplate, Paragraph, Spacer #type: ignore
from reportlab.lib.styles import getSampleStyleSheet #type: ignore
from django.utils.html import format_html #type: ignore



@shared_task
def send_order_html_email(order_data, email):
    BASE_URL = os.getenv('BASE_URL_BACKEND')  # Ensure this is set in your environment variables
    # Build the HTML content
    html_content = f"""
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; }}
            table {{ border-collapse: collapse; width: 100%; margin-bottom: 20px; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            h2 {{ color: #333; }}
        </style>
    </head>
    <body>
        <h2>Order Report - ID {order_data['id']}</h2>
        <h3>User Details</h3>
        <table>
            <tr><th>Full Name</th><td>{order_data['user']['full_name']}</td></tr>
            <tr><th>Email</th><td>{order_data['user']['email']}</td></tr>
            <tr><th>Phone</th><td>{order_data['user']['phone_number']}</td></tr>
        </table>

        <h3>Order Summary</h3>
        <table>
            <tr><th>Total Area</th><td>{float(order_data['tatalArea']):.0f}</td></tr>
            <tr><th>Material</th><td>{order_data['material']['name']}</td></tr>
            <tr><th>Thickness</th><td>{order_data['thickness']['name']}</td></tr>
            <tr><th>Color</th><td>{order_data['color']}</td></tr>
            <tr><th>Total Drilling Holes</th><td>{order_data['totalDrilingHoles']}</td></tr>
        </table>

        <h3>Plate Items</h3>
        <table>
            <tr>
                <th>Name</th>
                <th>Description</th>
            </tr>
    """
    for plate in order_data['plate_items']:
        icon_url = BASE_URL + plate['icon']  # full URL for email
        html_content += f"""
            <tr>
                <td>{plate['name']}</td>
                <td>{plate['description']}</td>
            </tr>
        """
    
    html_content += """
        </table>
        <p>Thank you for your order!</p>
    </body>
    </html>
    """

    # Send email
    mail = EmailMessage(
        subject=f"Order #{order_data['id']} Details",
        body=html_content,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
    )
    mail.content_subtype = "html"  # Important: this makes the email HTML
    mail.send()
    print(f"Order details email sent to {email} for order ID {order_data['id']}")

# @shared_task
# def send_order_pdf_email(order, email):

#     pdf_content = generate_order_pdf(order)

#     mail = EmailMessage(
#         subject="Your Order Details",
#         body="Please find attached the PDF with your order details.",
#         from_email=settings.DEFAULT_FROM_EMAIL,
#         to=[email],
#     )

#     mail.attach(
#         f"order_{order['id']}.pdf",
#         pdf_content,
#         "application/pdf"
#     )

#     mail.send()
    
    
# def generate_order_pdf(order):
#     buffer = io.BytesIO()
#     doc = SimpleDocTemplate(buffer, pagesize=letter)
#     elements = []
#     styles = getSampleStyleSheet()

#     # ===== Title =====
#     elements.append(Paragraph(f"Order Invoice - ID: {order['id']}", styles['Title']))
#     elements.append(Spacer(1, 12))

#     # ===== User Info =====
#     user = order['user']
#     user_info = [
#         ['Customer Name', user['full_name']],
#         ['Email', user['email']],
#         ['Phone', user.get('phone_number', '')],
#         # ['Order Date', order.get('created_at', '')],
#     ]
#     user_table = Table(user_info, hAlign='LEFT')
#     user_table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
#         ('GRID', (0,0), (-1,-1), 0.5, colors.black),
#     ]))
#     elements.append(Paragraph("Customer Info:", styles['Heading2']))
#     elements.append(user_table)
#     elements.append(Spacer(1, 12))

#     # ===== Material Info =====
#     material = order['material']
#     material_info = [
#         ['Material Name', material['name']],
#         ['Description', material.get('description','')],
#         ['Active', material.get('is_active', True)],
#     ]
#     material_table = Table(material_info, hAlign='LEFT')
#     material_table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
#         ('GRID', (0,0), (-1,-1), 0.5, colors.black),
#     ]))
#     elements.append(Paragraph("Material Info:", styles['Heading2']))
#     elements.append(material_table)
#     elements.append(Spacer(1, 6))
    

#     # ===== Material Variants =====
#     variants = material.get('variants', [])
#     if variants:
#         variants_data = [['ID', 'Name', 'Price', 'Active', 'Created', 'Updated']]
#         for v in variants:
#             variants_data.append([
#                 v['id'], v['name'], v['price'], v['is_active'], v['created_at'], v['updated_at']
#             ])
#         variant_table = Table(variants_data, hAlign='LEFT')
#         variant_table.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.grey),
#             ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.black),
#             ('FONTSIZE', (0,0), (-1,-1), 8),
#         ]))
#         elements.append(Paragraph("Material Variants:", styles['Heading3']))
#         elements.append(variant_table)
#         elements.append(Spacer(1, 12))

#     # ===== Thickness Info =====
#     thickness = order['thickness']
#     thickness_info = [
#         ['Thickness Name', thickness['name']],
#         ['Price', thickness.get('price', '')],
#         ['Active', thickness.get('is_active', True)],
#     ]
#     thickness_table = Table(thickness_info, hAlign='LEFT')
#     thickness_table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
#         ('GRID', (0,0), (-1,-1), 0.5, colors.black),
#     ]))
#     elements.append(Paragraph("Thickness Info:", styles['Heading2']))
#     elements.append(thickness_table)
#     elements.append(Spacer(1, 12))

#     # ===== Order Info =====
#     order_info = [
#         ['Total Area', order.get('tatalArea','')],
#         ['Total Perimeter', order.get('totalPerimeter','')],
#         ['Color', order.get('color','')],
#         ['Total Drilling Holes', order.get('totalDrilingHoles','')],
#         ['Total Price', order.get('total_price','')],
#     ]
#     order_table = Table(order_info, hAlign='LEFT')
#     order_table.setStyle(TableStyle([
#         ('BACKGROUND', (0,0), (0,-1), colors.lightgrey),
#         ('GRID', (0,0), (-1,-1), 0.5, colors.black),
#     ]))
#     elements.append(Paragraph("Order Info:", styles['Heading2']))
#     elements.append(order_table)
#     elements.append(Spacer(1, 12))

#     # ===== Plate Items =====
#     plate_items = order.get('plate_items', [])
#     if plate_items:
#         items_data = [['ID','Name','Description','Points','Drilling Holes','Closed','Created','Updated']]
#         for item in plate_items:
#             points = str(item.get('points', []))
#             holes = str(item.get('drillingHole', []))
#             items_data.append([
#                 item['id'],
#                 item.get('name',''),
#                 item.get('description',''),
#                 points,
#                 holes,
#                 'Yes' if item.get('closed', False) else 'No',
#                 item.get('created_at',''),
#                 item.get('updated_at','')
#             ])
#         item_table = Table(items_data, hAlign='LEFT')
#         item_table.setStyle(TableStyle([
#             ('BACKGROUND', (0,0), (-1,0), colors.grey),
#             ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
#             ('GRID', (0,0), (-1,-1), 0.5, colors.black),
#             ('FONTSIZE', (0,0), (-1,-1), 7),
#         ]))
#         elements.append(Paragraph("Plate Items:", styles['Heading2']))
#         elements.append(item_table)
#         elements.append(Spacer(1, 12))

#     # ===== Build PDF =====
#     doc.build(elements)
#     buffer.seek(0)
#     return buffer.getvalue()