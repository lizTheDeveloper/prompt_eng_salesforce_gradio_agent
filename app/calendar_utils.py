import datetime
from app.google_auth import get_google_services


def get_week_range(target_date):
    """
    Given a date (datetime.date), return the start and end datetime objects for that week (Monday-Sunday).
    """
    start_of_week = target_date - datetime.timedelta(days=target_date.weekday())
    end_of_week = start_of_week + datetime.timedelta(days=6)
    start_datetime = datetime.datetime.combine(start_of_week, datetime.time.min)
    end_datetime = datetime.datetime.combine(end_of_week, datetime.time.max)
    return start_datetime, end_datetime


def fetch_and_classify_meetings_for_week(target_date):
    """
    Fetch all meetings for the week containing target_date from Google Calendar.
    Classify each as 'recurring' or 'one-off'.
    Returns a list of dicts: { 'summary', 'start', 'end', 'type', 'id', 'attendees' }
    """
    calendar_service, _ = get_google_services()
    start_datetime, end_datetime = get_week_range(target_date)
    events_result = calendar_service.events().list(
        calendarId='primary',
        timeMin=start_datetime.isoformat() + 'Z',
        timeMax=end_datetime.isoformat() + 'Z',
        singleEvents=True,
        orderBy='startTime',
    ).execute()
    events = events_result.get('items', [])
    meeting_list = []
    for event in events:
        event_type = 'recurring' if 'recurringEventId' in event or 'recurrence' in event else 'one-off'
        attendees = []
        for attendee in event.get('attendees', []):
            email = attendee.get('email')
            if email:
                attendees.append(email)
        meeting_list.append({
            'summary': event.get('summary', '(No Title)'),
            'start': event['start'].get('dateTime', event['start'].get('date')),
            'end': event['end'].get('dateTime', event['end'].get('date')),
            'type': event_type,
            'id': event.get('id'),
            'attendees': attendees,
        })
    return meeting_list


def cancel_meetings(
    meeting_ids=None,
    target_date=None,
    date_range=None,
    meeting_type=None,
    summary_keywords=None,
    logger=None,
):
    """
    Cancel (delete) meetings from Google Calendar with flexible filters.
    - meeting_ids: list of event IDs to cancel
    - target_date: a single date (datetime.date) to cancel meetings on
    - date_range: tuple of (start_date, end_date) to cancel meetings in range
    - meeting_type: 'recurring', 'one-off', or None for both
    - summary_keywords: list of keywords to match in meeting summary
    Returns a list of dicts: { 'summary', 'id', 'status', 'error' }
    """
    calendar_service, _ = get_google_services()
    meetings = []
    # Fetch meetings based on date or range
    if target_date:
        meetings = fetch_and_classify_meetings_for_week(target_date)
    elif date_range:
        start_date, end_date = date_range
        current_date = start_date
        while current_date <= end_date:
            meetings.extend(fetch_and_classify_meetings_for_week(current_date))
            current_date += datetime.timedelta(days=7)
    else:
        # If no date provided, fetch for current week
        meetings = fetch_and_classify_meetings_for_week(datetime.date.today())
    # Filter meetings
    filtered_meetings = []
    for meeting in meetings:
        if meeting_ids and meeting['id'] not in meeting_ids:
            continue
        if meeting_type and meeting['type'] != meeting_type:
            continue
        if summary_keywords and not any(kw.lower() in meeting['summary'].lower() for kw in summary_keywords):
            continue
        filtered_meetings.append(meeting)
    # If meeting_ids provided but not found in fetched meetings, add them directly
    if meeting_ids:
        fetched_ids = {m['id'] for m in filtered_meetings}
        for meeting_id in meeting_ids:
            if meeting_id not in fetched_ids:
                filtered_meetings.append({'id': meeting_id, 'summary': '(Unknown)', 'type': None})
    # Cancel filtered meetings
    results = []
    for meeting in filtered_meetings:
        try:
            calendar_service.events().delete(
                calendarId='primary',
                eventId=meeting['id']
            ).execute()
            result = {'summary': meeting.get('summary', '(No Title)'), 'id': meeting['id'], 'status': 'cancelled', 'error': None}
            if logger:
                logger.info(f"Cancelled meeting: {meeting.get('summary', '(No Title)')} ({meeting['id']})")
        except Exception as error:
            result = {'summary': meeting.get('summary', '(No Title)'), 'id': meeting['id'], 'status': 'error', 'error': str(error)}
            if logger:
                logger.error(f"Error cancelling meeting {meeting.get('summary', '(No Title)')} ({meeting['id']}): {error}")
        results.append(result)
    return results


def cancel_recurring_meetings_for_week(target_date, logger=None):
    """
    Cancel (delete) all recurring meetings for the week containing target_date.
    Logs each action and error if a logger is provided.
    Returns a list of dicts: { 'summary', 'id', 'status', 'error' }
    """
    return cancel_meetings(target_date=target_date, meeting_type='recurring', logger=logger) 