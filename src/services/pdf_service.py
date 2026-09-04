"""
PDF Export Service for School Management System
Generates professional PDFs for report cards, timetables, and invoices
"""

from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_RIGHT
from datetime import date
from pathlib import Path
from typing import List, Dict, Optional
import logging

logger = logging.getLogger(__name__)


class PDFService:
    """Service for generating PDF reports"""

    def __init__(self):
        self.styles = getSampleStyleSheet()
        self.page_width, self.page_height = A4
        self.setup_custom_styles()

    def setup_custom_styles(self):
        """Setup custom paragraph styles"""
        self.styles.add(ParagraphStyle(
            name='Title',
            parent=self.styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#1a1a1a'),
            spaceAfter=12,
            alignment=TA_CENTER,
            fontName='Helvetica-Bold'
        ))

        self.styles.add(ParagraphStyle(
            name='Subtitle',
            parent=self.styles['Normal'],
            fontSize=11,
            textColor=colors.HexColor('#333333'),
            spaceAfter=6,
            alignment=TA_CENTER
        ))

        self.styles.add(ParagraphStyle(
            name='SectionHeader',
            parent=self.styles['Heading2'],
            fontSize=12,
            textColor=colors.HexColor('#1a5490'),
            spaceAfter=8,
            spaceBefore=8,
            fontName='Helvetica-Bold'
        ))

    def generate_student_report_card(self, student, exam_results, filepath: Path):
        """
        Generate individual student report card

        Args:
            student: Student object
            exam_results: List of exam result dicts with subject, marks, grade, gpa
            filepath: Output PDF file path
        """
        try:
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=A4,
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )

            story = []

            # Header
            header_data = [
                [Paragraph(f"<b>SCHOOL MANAGEMENT SYSTEM</b>", self.styles['Title'])],
                [Paragraph(f"Progress Report Card - {date.today().strftime('%B %Y')}",
                          self.styles['Subtitle'])],
            ]
            header_table = Table(header_data, colWidths=[7*inch])
            header_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
            ]))
            story.append(header_table)
            story.append(Spacer(1, 0.2*inch))

            # Student information
            student_info = [
                ['Student Name:', student.full_name, 'Admission #:', student.admission_number],
                ['Roll Number:', student.roll_number, 'Class:', getattr(student, 'class_name', '')],
                ['Date of Birth:', student.date_of_birth.strftime("%d-%m-%Y") if student.date_of_birth else '',
                 'Gender:', student.gender],
            ]

            info_table = Table(student_info, colWidths=[1.5*inch, 2*inch, 1.5*inch, 2*inch])
            info_table.setStyle(TableStyle([
                ('FONT', (0, 0), (0, -1), 'Helvetica-Bold', 10),
                ('FONT', (2, 0), (2, -1), 'Helvetica-Bold', 10),
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('BORDER', (0, 0), (-1, -1), 0.5, colors.grey),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#e8e8e8')),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ('LEFTPADDING', (0, 0), (-1, -1), 6),
                ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(info_table)
            story.append(Spacer(1, 0.2*inch))

            # Marks table
            story.append(Paragraph("Academic Performance", self.styles['SectionHeader']))

            marks_data = [['Subject', 'Marks Obtained', 'Total Marks', 'Percentage', 'Grade', 'GPA']]
            total_marks = 0
            total_obtained = 0

            for result in exam_results:
                marks_data.append([
                    result.get('subject', ''),
                    str(result.get('marks_obtained', 0)),
                    str(result.get('total_marks', 0)),
                    f"{result.get('percentage', 0):.1f}%",
                    result.get('grade', '-'),
                    f"{result.get('gpa', 0):.2f}"
                ])
                total_obtained += result.get('marks_obtained', 0)
                total_marks += result.get('total_marks', 0)

            marks_data.append([
                'Total',
                str(total_obtained),
                str(total_marks),
                f"{(total_obtained/total_marks*100):.1f}%" if total_marks > 0 else '0%',
                '-',
                '-'
            ])

            marks_table = Table(marks_data, colWidths=[1.8*inch, 1.2*inch, 1.2*inch, 1.2*inch, 0.8*inch, 0.8*inch])
            marks_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 10),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
                ('BORDER', (0, 0), (-1, -1), 0.5, colors.grey),
                ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.HexColor('#f5f5f5')]),
                ('BACKGROUND', (0, -1), (-1, -1), colors.HexColor('#d9d9d9')),
                ('FONT', (0, -1), (-1, -1), 'Helvetica-Bold', 9),
                ('TOPPADDING', (0, 0), (-1, -1), 6),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
            ]))
            story.append(marks_table)
            story.append(Spacer(1, 0.2*inch))

            # Footer
            story.append(Spacer(1, 0.3*inch))
            footer_data = [
                ['Teacher Signature', 'Principal Signature', 'Guardian Signature'],
                ['___________________', '___________________', '___________________'],
                [f"Date: {date.today().strftime('%d-%m-%Y')}", '', ''],
            ]
            footer_table = Table(footer_data, colWidths=[2.3*inch, 2.3*inch, 2.3*inch])
            footer_table.setStyle(TableStyle([
                ('ALIGN', (0, 0), (-1, 0), 'CENTER'),
                ('FONTSIZE', (0, 0), (-1, -1), 9),
                ('BORDER', (0, 0), (-1, -1), 0, colors.white),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(footer_table)

            # Generate PDF
            doc.build(story)
            logger.info(f"Report card generated: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to generate report card: {e}")
            raise

    def generate_timetable_pdf(self, timetable_data: Dict, filepath: Path):
        """
        Generate printable timetable

        Args:
            timetable_data: Dictionary with timetable information
            filepath: Output PDF file path
        """
        try:
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=landscape(A4),
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )

            story = []

            # Header
            story.append(Paragraph(
                f"<b>CLASS TIMETABLE - {timetable_data.get('class_name', 'Class')}</b>",
                self.styles['Title']
            ))
            story.append(Paragraph(
                f"Section: {timetable_data.get('section_name', '')}" +
                f" | Academic Year: {date.today().year}",
                self.styles['Subtitle']
            ))
            story.append(Spacer(1, 0.2*inch))

            # Timetable grid
            periods = timetable_data.get('periods', [])
            days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday']

            timetable_data_rows = [['Period / Time'] + days]

            for period in periods:
                row = [f"{period['number']}\n{period['start']}-{period['end']}"]
                for day in days:
                    # Find entry for this day and period
                    entry = next(
                        (p for p in period.get('entries', []) if p['day'] == day),
                        None
                    )
                    if entry:
                        row.append(f"{entry['subject']}\n({entry['teacher']})\n{entry['room']}")
                    else:
                        row.append('-')
                timetable_data_rows.append(row)

            col_widths = [1*inch] + [1.3*inch]*6
            tt_table = Table(timetable_data_rows, colWidths=col_widths)
            tt_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
                ('BORDER', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(tt_table)

            doc.build(story)
            logger.info(f"Timetable PDF generated: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to generate timetable: {e}")
            raise

    def generate_fee_invoice(self, invoice_data: Dict, filepath: Path):
        """
        Generate fee invoice/challan

        Args:
            invoice_data: Dictionary with invoice details
            filepath: Output PDF file path
        """
        try:
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=landscape(A4),
                rightMargin=0.25*inch,
                leftMargin=0.25*inch,
                topMargin=0.25*inch,
                bottomMargin=0.25*inch
            )

            story = []

            # Three-part challan
            challan_data = [
                ['BANK COPY', 'SCHOOL COPY', 'STUDENT COPY'],
            ]

            for idx in range(3):
                # Invoice header
                header = f"""
                <b>SCHOOL MANAGEMENT SYSTEM - FEE CHALLAN</b><br/>
                Invoice #: {invoice_data.get('invoice_number', '')}<br/>
                Date: {date.today().strftime('%d-%m-%Y')}
                """

                # Student details
                student_info = f"""
                <b>Student Name:</b> {invoice_data.get('student_name', '')}<br/>
                <b>Admission #:</b> {invoice_data.get('admission_number', '')}<br/>
                <b>Class:</b> {invoice_data.get('class_name', '')}<br/>
                <b>Due Date:</b> {invoice_data.get('due_date', '')}
                """

                # Amount details
                amount_info = f"""
                <b>Tuition Fee:</b> ₹{invoice_data.get('tuition_fee', 0)}<br/>
                <b>Lab Fee:</b> ₹{invoice_data.get('lab_fee', 0)}<br/>
                <b>Arrears:</b> ₹{invoice_data.get('arrears', 0)}<br/>
                <b>Discount:</b> -₹{invoice_data.get('discount', 0)}<br/>
                <b>Total Due:</b> <b>₹{invoice_data.get('total_amount', 0)}</b>
                """

            doc.build(story)
            logger.info(f"Invoice PDF generated: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to generate invoice: {e}")
            raise

    def generate_bulk_report_cards(self, students_data: List[Dict], output_dir: Path):
        """
        Generate bulk report cards for multiple students

        Args:
            students_data: List of student data dictionaries
            output_dir: Output directory for PDFs
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            generated_files = []

            for student_data in students_data:
                filename = f"reportcard_{student_data.get('admission_number', 'unknown')}.pdf"
                filepath = output_dir / filename

                self.generate_student_report_card(
                    student_data.get('student'),
                    student_data.get('exam_results', []),
                    filepath
                )
                generated_files.append(filepath)

            logger.info(f"Generated {len(generated_files)} report cards")
            return generated_files

        except Exception as e:
            logger.error(f"Bulk report card generation failed: {e}")
            raise

    def generate_master_tabulation_sheet(self, class_results: List[Dict], filepath: Path):
        """
        Generate master tabulation/gazette for class results

        Args:
            class_results: List of student results with rankings
            filepath: Output PDF file path
        """
        try:
            doc = SimpleDocTemplate(
                str(filepath),
                pagesize=landscape(A4),
                rightMargin=0.5*inch,
                leftMargin=0.5*inch,
                topMargin=0.5*inch,
                bottomMargin=0.5*inch
            )

            story = []

            # Header
            story.append(Paragraph(
                f"<b>MASTER TABULATION SHEET - {class_results[0].get('class_name', 'Class')}</b>",
                self.styles['Title']
            ))
            story.append(Paragraph(
                f"Academic Year: {date.today().year} | Generated: {date.today().strftime('%d-%m-%Y')}",
                self.styles['Subtitle']
            ))
            story.append(Spacer(1, 0.2*inch))

            # Results table
            headers = ['Rank', 'Admission #', 'Student Name', 'Total Marks', 'Percentage', 'Grade', 'Status']
            table_data = [headers]

            for result in class_results:
                table_data.append([
                    str(result.get('rank', '-')),
                    result.get('admission_number', ''),
                    result.get('student_name', ''),
                    str(result.get('total_marks', 0)),
                    f"{result.get('percentage', 0):.1f}%",
                    result.get('grade', '-'),
                    result.get('status', 'PASS')
                ])

            col_widths = [0.8*inch, 1.2*inch, 2*inch, 1.2*inch, 1.2*inch, 0.8*inch, 1*inch]
            results_table = Table(table_data, colWidths=col_widths)
            results_table.setStyle(TableStyle([
                ('FONT', (0, 0), (-1, 0), 'Helvetica-Bold', 9),
                ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#1a5490')),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('ALIGN', (2, 1), (2, -1), 'LEFT'),
                ('BORDER', (0, 0), (-1, -1), 0.5, colors.grey),
                ('FONTSIZE', (0, 0), (-1, -1), 8),
                ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f5f5f5')]),
                ('TOPPADDING', (0, 0), (-1, -1), 4),
                ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ]))
            story.append(results_table)

            doc.build(story)
            logger.info(f"Master tabulation sheet generated: {filepath}")
            return filepath

        except Exception as e:
            logger.error(f"Failed to generate master sheet: {e}")
            raise


if __name__ == "__main__":
    print("PDF Service module loaded")
