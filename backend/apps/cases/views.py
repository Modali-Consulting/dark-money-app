from io import BytesIO

from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

from .models import CaseFile, CaseResource, EvidenceItem
from .serializers import CaseFileSerializer, CaseResourceSerializer, EvidenceItemSerializer


class CaseFileViewSet(viewsets.ModelViewSet):
    queryset = CaseFile.objects.all().order_by("-created_at")
    serializer_class = CaseFileSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class EvidenceItemViewSet(viewsets.ModelViewSet):
    queryset = EvidenceItem.objects.select_related("case", "resource").all().order_by("-created_at")
    serializer_class = EvidenceItemSerializer
    permission_classes = [IsAuthenticated]


class CaseResourceViewSet(viewsets.ModelViewSet):
    queryset = CaseResource.objects.select_related("case", "resource").all()
    serializer_class = CaseResourceSerializer
    permission_classes = [IsAuthenticated]


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def export_case_pdf(request, pk):
    case = CaseFile.objects.get(pk=pk)
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle(f"Case Brief - {case.title}")

    y = 750
    pdf.setFont("Helvetica-Bold", 16)
    pdf.drawString(50, y, f"Case Brief: {case.title}")
    y -= 30

    pdf.setFont("Helvetica", 11)
    pdf.drawString(50, y, f"Status: {case.status}")
    y -= 20
    pdf.drawString(50, y, f"Hypothesis: {case.hypothesis}")
    y -= 30

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Evidence Log")
    y -= 20

    for evidence in case.evidence.all():
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y, f"- {evidence.title}: {evidence.claim_summary}")
        y -= 15
        if y < 100:
            pdf.showPage()
            y = 750

    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Saved Resources")
    y -= 20

    for saved in case.saved_resources.all():
        pdf.setFont("Helvetica", 10)
        pdf.drawString(50, y, f"- {saved.resource.name}")
        y -= 15
        if y < 100:
            pdf.showPage()
            y = 750

    pdf.showPage()
    pdf.save()

    buffer.seek(0)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = f"attachment; filename=case_{case.id}_brief.pdf"
    return response
