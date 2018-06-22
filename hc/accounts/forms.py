from django import forms


class LowercaseEmailField(forms.EmailField):

    def clean(self, value):
        value = super(LowercaseEmailField, self).clean(value)
        return value.lower()


class EmailPasswordForm(forms.Form):
    email = LowercaseEmailField()
    password = forms.CharField(required=False)


class ReportSettingsForm(forms.Form):
    reports_allowed = forms.BooleanField(required=False)
    report_period = forms.IntegerField()


class SetPasswordForm(forms.Form):
    password = forms.CharField()


class InviteTeamMemberForm(forms.Form):
    email = LowercaseEmailField()
    check = forms.CharField()


class RemoveTeamMemberForm(forms.Form):
    email = LowercaseEmailField()


class TeamNameForm(forms.Form):
    team_name = forms.CharField(max_length=200, required=True)


class AlertForm(forms.Form):
    alert_mode = forms.CharField(required=True)
    phone_number = forms.CharField(required=True)
    

class SetPriorityForm(forms.Form):
    member_email = forms.CharField(max_length=200)
    priority = forms.CharField(max_length=10)

