from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from apps.clients.models import Client
from apps.channels.models import Channel, ChannelType
from apps.projects.models import Project, ProjectChannel, ProjectStep


class Command(BaseCommand):
    help = "Populates the database with sample data"

    def handle(self, *args, **options):
        self.stdout.write("Creating sample data...")

        # Create channel types
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

        # Create projects
        statuses = ["DRAFT", "IN_PROGRESS", "ON_HOLD", "COMPLETED", "CANCELLED"]
        status_weights = [0.1, 0.3, 0.2, 0.3, 0.1]  # Probability weights for statuses

        today = timezone.now().date()

        for i in range(25):
            # Randomize dates
            days_offset = random.randint(-60, 60)  # Projects within ±60 days from today
            start_date = today + timedelta(days=days_offset)
            duration = random.randint(7, 90)  # Projects lasting 7-90 days

            project = Project.objects.create(
                name=f"Project {i+1}",
                client=random.choice(clients),
                status=random.choices(statuses, weights=status_weights)[0],
                deadline=start_date + timedelta(days=duration),
                cost=random.randint(5000, 50000),
                description=f"Sample project description {i+1}" if i % 2 == 0 else "",
            )

            # Add 1-3 channels to each project
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

            # Add 3-7 steps to each project
            num_steps = random.randint(3, 7)
            for j in range(num_steps):
                is_completed = random.random() < 0.6 if project.status in ["COMPLETED", "IN_PROGRESS"] else False
                step_deadline = start_date + timedelta(days=random.randint(1, duration))

                ProjectStep.objects.create(
                    project=project,
                    name=f"Step {j+1}",
                    description=f"Step description {j+1}" if j % 2 == 0 else "",
                    is_completed=is_completed,
                    due_date=step_deadline,
                    order=j + 1,
                )

        self.stdout.write(self.style.SUCCESS("Successfully created sample data"))
        self.stdout.write(f"Created:")
        self.stdout.write(f"- {len(channel_types)} channel types")
        self.stdout.write(f"- {len(channels)} channels")
        self.stdout.write(f"- {len(clients)} clients")
        self.stdout.write(f"- 25 projects with varying statuses")
