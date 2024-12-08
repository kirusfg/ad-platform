from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta, datetime, time
import random

from apps.clients.models import Client
from apps.channels.models import Channel, ChannelType
from apps.projects.models import Project, ProjectChannel, ProjectStep
from apps.events.models import Event, EventType, EventStatus


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **options):
        # First, clear the database
        self.stdout.write("Clearing existing data...")
        Event.objects.all().delete()
        EventType.objects.all().delete()
        EventStatus.objects.all().delete()
        Project.objects.all().delete()
        Client.objects.all().delete()
        Channel.objects.all().delete()
        ChannelType.objects.all().delete()

        self.stdout.write("Creating sample data...")

        # [Keep all existing channel types, channels, clients, and projects creation code]
        channel_types = [
            ChannelType.objects.create(name="LED Screen"),
            ChannelType.objects.create(name="Billboard"),
            ChannelType.objects.create(name="Social Media"),
            ChannelType.objects.create(name="TV"),
            ChannelType.objects.create(name="Radio"),
        ]

        # Create channels
        channels = []
        locations = ["Downtown", "Shopping Mall", "Business Center", "Stadium", "Airport"]
        for i in range(15):
            channel = Channel.objects.create(
                name=f"Channel {i+1}",
                type=random.choice(channel_types),
                status=random.choice(["FREE", "RESERVED", "IN_USE", "BLOCKED"]),
                location=random.choice(locations),
                technical_specs=f'Resolution: {random.choice(["4K", "1080p", "720p"])}' if i % 2 == 0 else "",
                comments=f"Sample comment for channel {i+1}" if i % 3 == 0 else "",
            )
            channels.append(channel)

        # Create clients
        clients = []
        company_types = ["LLC", "Inc.", "Corp", "Company"]
        for i in range(10):
            client = Client.objects.create(
                name=f"Company {i+1} {random.choice(company_types)}",
                contact_person=f"Contact Person {i+1}",
                email=f"contact{i+1}@company{i+1}.com",
                phone=f"+7 ({random.randint(700,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}",
                address=f"Street {i+1}, City" if i % 2 == 0 else "",
                notes=f"Important client notes {i+1}" if i % 3 == 0 else "",
            )
            clients.append(client)

        # [Keep existing projects creation code]
        statuses = ["DRAFT", "IN_PROGRESS", "ON_HOLD", "COMPLETED", "CANCELLED"]
        status_weights = [0.1, 0.3, 0.2, 0.3, 0.1]

        today = timezone.now().date()

        # Create projects
        for i in range(300):
            # [Keep existing project creation code]
            days_offset = random.randint(-365, 365)
            start_date = today + timedelta(days=days_offset)
            duration = random.randint(7, 90)

            if days_offset < -90:
                status = random.choices(statuses, weights=[0.05, 0.05, 0.1, 0.7, 0.1])[0]
            elif days_offset > 0:
                status = random.choices(statuses, weights=[0.6, 0.2, 0.1, 0, 0.1])[0]
            else:
                status = random.choices(statuses, weights=status_weights)[0]

            project = Project.objects.create(
                name=f"Project {i+1}",
                client=random.choice(clients),
                status=status,
                deadline=start_date + timedelta(days=duration),
                cost=random.randint(5000, 50000),
                description=f"Sample project description {i+1}" if i % 2 == 0 else "",
                created_at=timezone.make_aware(datetime.combine(start_date, datetime.min.time())),
            )

            # [Keep existing project channels and steps creation code]
            for _ in range(random.randint(1, 3)):
                channel = random.choice(channels)
                channel_duration = random.randint(7, duration)
                channel_start = start_date + timedelta(days=random.randint(0, duration - channel_duration))

                ProjectChannel.objects.create(
                    project=project,
                    channel=channel,
                    start_date=channel_start,
                    end_date=channel_start + timedelta(days=channel_duration),
                    cost=random.randint(1000, 10000),
                )

            num_steps = random.randint(3, 7)
            for j in range(num_steps):
                is_completed = (
                    random.random() < 0.8 if status == "COMPLETED" else (random.random() < 0.6 if status == "IN_PROGRESS" else False)
                )
                step_deadline = start_date + timedelta(days=random.randint(1, duration))

                ProjectStep.objects.create(
                    project=project,
                    name=f"Step {j+1}",
                    description=f"Step description {j+1}" if j % 2 == 0 else "",
                    is_completed=is_completed,
                    due_date=step_deadline,
                    order=j + 1,
                )

        # Create event types and statuses
        event_types = [
            EventType.objects.create(name="Client Meeting"),
            EventType.objects.create(name="Ad Installation"),
            EventType.objects.create(name="Team Meeting"),
            EventType.objects.create(name="Conference"),
            EventType.objects.create(name="Phone Call"),
        ]

        event_statuses = [
            EventStatus.objects.create(name="Planned"),
            EventStatus.objects.create(name="Confirmed"),
            EventStatus.objects.create(name="Completed"),
            EventStatus.objects.create(name="Cancelled"),
        ]

        # Create events
        business_hours = [(9, 0), (10, 30), (11, 0), (14, 0), (15, 30), (16, 0)]
        event_durations = [30, 60, 90, 120]  # Duration in minutes

        # Create 200 events
        for i in range(200):
            days_offset = random.randint(-180, 180)  # ±6 months
            event_date = today + timedelta(days=days_offset)
            hour, minute = random.choice(business_hours)
            duration = random.choice(event_durations)

            start_datetime = datetime.combine(event_date, time(hour, minute))
            end_datetime = start_datetime + timedelta(minutes=duration)

            if event_date < today:
                status = event_statuses[2]  # Completed
            elif event_date == today:
                status = event_statuses[1]  # Confirmed
            else:
                status = random.choice(event_statuses[:2])  # Planned or Confirmed

            event_type = random.choice(event_types)

            if event_type.name == "Client Meeting":
                title = f"Meeting with {random.choice(clients).name}"
            elif event_type.name == "Ad Installation":
                title = f"Install ads at {random.choice(channels).location}"
            elif event_type.name == "Conference":
                title = f"Conference: Digital Advertising {event_date.year}"
            elif event_type.name == "Phone Call":
                title = f"Call with {random.choice(clients).contact_person}"
            else:
                title = f"{event_type.name} #{i+1}"

            Event.objects.create(
                title=title,
                description=f"Event description {i+1}",
                type=event_type,
                status=status,
                start_datetime=timezone.make_aware(start_datetime),
                end_datetime=timezone.make_aware(end_datetime),
                project=random.choice(list(Project.objects.all()) + [None] * 3),
                channel=random.choice(list(Channel.objects.all()) + [None] * 4),
            )

        self.stdout.write(self.style.SUCCESS("Successfully created sample data"))
        self.stdout.write(f"Created:")
        self.stdout.write(f"- {len(channel_types)} channel types")
        self.stdout.write(f"- {len(channels)} channels")
        self.stdout.write(f"- {len(clients)} clients")
        self.stdout.write(f"- {Project.objects.count()} projects")
        self.stdout.write(f"- {len(event_types)} event types")
        self.stdout.write(f"- {len(event_statuses)} event statuses")
        self.stdout.write(f"- {Event.objects.count()} events")
