"""Define PDF Export."""

# from easy_pdf.views import PDFTemplateView

# from .. events.choices import (
#     EventStatus,
#     ParticipationStatus)
# from .. events.models import Participation


# class CompletedEventsPDF(PDFTemplateView):
#     """Export the List of the completed Events to PDF."""

#     template_name = "accounts/export/my-profile-completed-events-export.html"

#     def get_context_data(self, **kwargs):
#         completed_participations = Participation.objects.filter(
#             user=self.request.user,
#             event__status=EventStatus.COMPLETE,
#             status__in=[
#                 ParticipationStatus.WAITING_FOR_SELFREFLECTION,
#                 ParticipationStatus.WAITING_FOR_ACKNOWLEDGEMENT,
#                 ParticipationStatus.ACKNOWLEDGED,
#             ]
#         )

#         return super().get_context_data(
#             pagesize="A4",
#             title="Hi there!",
#             completed_participations=completed_participations,
#             **kwargs)
