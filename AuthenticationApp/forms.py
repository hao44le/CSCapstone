"""AuthenticationApp Forms

Created by Naman Patwari on 10/4/2016.
"""
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django import forms
from .models import MyUser

class LoginForm(forms.Form):
    email = forms.CharField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)


class RegisterForm(forms.Form):
    """A form to creating new users. Includes all the required
    fields, plus a repeated password."""
    email = forms.CharField(label='Email', widget=forms.EmailInput, required=True)
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, required=True)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput, required=True)    

    firstname = forms.CharField(label="First name", widget=forms.TextInput, required=False)
    lastname = forms.CharField(label="Last name", widget=forms.TextInput, required=False)     

    contact_info = forms.CharField(label="Contact Information", widget=forms.TextInput, required=False)
    description = forms.CharField(label="Description", widget=forms.Textarea, required=False)

    student = forms.NullBooleanField(label="Is student?", widget=forms.NullBooleanSelect, required=False)       
    professor = forms.NullBooleanField(label="Is professor?", widget=forms.NullBooleanSelect, required=False)     
    engineer = forms.NullBooleanField(label="Is engineer?", widget=forms.NullBooleanSelect, required=False)

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

    def clean(self):
        is_student = self.cleaned_data.get("student")
        is_professor = self.cleaned_data.get("professor")
        is_engineer = self.cleaned_data.get("engineer")
        #Classify the Users as Students, Professors, Engineers
        if is_student == True and is_professor == True and is_engineer == True:
            raise forms.ValidationError("User cannot be Student, Professor and Enginner at the same time!")
        elif is_student == True and is_engineer == True:
            raise forms.ValidationError("User cannot be Student and Enginner at the same time!")
        elif is_student == True and is_professor == True:
            raise forms.ValidationError("User cannot be Student and Professor at the same time!")
        elif is_engineer == True and is_professor == True:
            raise forms.ValidationError("User cannot be Professor and Enginner at the same time!")


class UpdateForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser        
        fields = ('email', 'password', 'first_name', 'last_name','contact_info','description','is_student', 'is_professor', 'is_engineer')
        widgets = { 
            'description': forms.Textarea()
        }
    def clean_password(self):            
        return self.initial["password"]        

    def clean_email(self):
        email = self.cleaned_data.get("email")
        #Check is email has changed
        if email == self.initial["email"]:
            return email
        #Check if email exists before
        try:
            exists = MyUser.objects.get(email=email)
            raise forms.ValidationError("This email has already been taken")
        except MyUser.DoesNotExist:
            return email
        except:
            raise forms.ValidationError("There was an error, please contact us later")

    def clean_first_name(self):
        first_name = self.cleaned_data.get("first_name")
        #Check is email has changed
        if first_name is None or first_name == "" or first_name == '':  
            email = self.cleaned_data.get("email")                               
            return email[:email.find("@")]      
        return first_name 

    def clean_is_student(self):
        is_student = self.cleaned_data.get("is_student")
        if is_student is not True:      
            return False
        return True 

    def clean_is_professor(self):
        is_professor = self.cleaned_data.get("is_professor")
        if is_professor is not True:      
            return False
        return True 

    def clean_is_engineer(self):
        is_engineer = self.cleaned_data.get("is_engineer")
        if is_engineer is not True:      
            return False
        return True                 

    def clean(self):
        is_student = self.cleaned_data.get("is_student")
        is_professor = self.cleaned_data.get("is_professor")
        is_engineer = self.cleaned_data.get("is_engineer")
        #Classify the Users as Students, Professors, Engineers
        if is_student == True and is_professor == True and is_engineer == True:
            raise forms.ValidationError("User cannot be Student, Professor and Enginner at the same time!")
        elif is_student == True and is_engineer == True:
            raise forms.ValidationError("User cannot be Student and Enginner at the same time!")
        elif is_student == True and is_professor == True:
            raise forms.ValidationError("User cannot be Student and Professor at the same time!")
        elif is_engineer == True and is_professor == True:
            raise forms.ValidationError("User cannot be Professor and Enginner at the same time!")


"""Admin Forms"""

class AdminUserCreationForm(forms.ModelForm):
    """A form for Admin to creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)    

    class Meta:
        model = MyUser
        fields = ('email', 'first_name', 'last_name','contact_info','description', 'is_student', 'is_professor', 'is_engineer')        

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(AdminUserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for Admin for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        #fields = ('email', 'password', 'first_name', 'last_name', 'is_active', 'is_admin')
        fields = ('email', 'password', 'first_name', 'last_name','contact_info','description', 'is_active', 'is_admin', 'is_student', 'is_professor', 'is_engineer')

    def clean_password(self):
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]        
