from django.db import models

YesNoChoices = [
    (None, 'All'),
    (True, 'Yes'),
    (False, 'No'),
]


class LeagueJoinRequestStatusChoices(models.TextChoices):
    PENDING = 'P', 'Pending'
    ACCEPTED = 'A', 'Accepted'
    REJECTED = 'R', 'Rejected'


class MatchStatusChoices(models.TextChoices):
    NOT_STARTED = 'NS', 'Not Started'
    IS_NEXT = 'IN', 'Is Next'
    IN_PROGRESS = 'IP', 'In Progress'
    COMPLETED = 'C', 'Completed'
    CANCELLED = 'X', 'Cancelled'


class GameWeekStatusChoices(models.TextChoices):
    NOT_STARTED = 'NS', 'Not Started'
    IS_NEXT = 'IN', 'Is Next'
    IN_PROGRESS = 'IP', 'In Progress'
    COMPLETED = 'C', 'Completed'


class CricketPositions:
    BATSMAN = 'Batsman'
    BOWLER = 'Bowler'
    ALL_ROUNDER = 'All-Rounder'
    WICKET_KEEPER = 'Wicket-Keeper'


class FootballPositions:
    GOAL_KEEPER = 'Goal-Keeper'
    DEFENDER = 'Defender'
    MID_FIELDER = 'Midfielder'
    FORWARD = 'Forward'


class AuthProviderChoices(models.TextChoices):
    GOOGLE = 'google', 'Google'
    EMAIL_PASS = 'email_pass', 'Email & Password'
