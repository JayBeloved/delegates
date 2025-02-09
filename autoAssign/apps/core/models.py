from django.db import models

class Delegate(models.Model):
    USER_TYPE_CHOICES = [
        ('nigerian', 'Nigerian Delegate (₦70,000)'),
        ('RUN', "Redeemer's University (₦55,000)"),
        ('foreign', 'International Delegate ($100)'),
    ]

    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]

    TSHIRT_SIZE_CHOICES = [
        ('xs', 'XS'),
        ('s', 'S'),
        ('m', 'M'),
        ('l', 'L'),
        ('xl', 'XL'),
        ('xxl', 'XXL'),
    ]

    ADVERT_CHOICES = [
        ('facebook', 'Facebook'),
        ('twitter', 'Twitter'),
        ('whatsapp', 'WhatsApp'),
        ('instagram', 'Instagram'),
        ('friend/colleague', 'Friend/Colleague'),
        ('university/institution', 'University/Institution'),
        ('ambassador', 'Campus Ambassador'),
        ('other', 'Other'),
    ]

    user_id = models.CharField(max_length=100, unique=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    delegate_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    mun_experience = models.TextField(blank=True, null=True)
    affiliation = models.CharField(max_length=250, blank=True, null=True)
    position = models.CharField(max_length=250, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)
    matric_num = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=200, blank=True, null=True)
    country = models.CharField(max_length=200, blank=True, null=True)
    zipcode = models.CharField(max_length=50, blank=True, null=True)
    advert = models.CharField(max_length=200, blank=True, null=True, choices=ADVERT_CHOICES)
    tshirt_size = models.CharField(max_length=10, blank=True, null=True, choices=TSHIRT_SIZE_CHOICES)
    medical = models.TextField(blank=True, null=True)
    diet = models.TextField(blank=True, null=True)
    referral = models.CharField(max_length=250, blank=True, null=True)
    committee1 = models.CharField(max_length=250, blank=True, null=True)
    country1 = models.CharField(max_length=250, blank=True, null=True)
    committee2 = models.CharField(max_length=250, blank=True, null=True)
    country2 = models.CharField(max_length=250, blank=True, null=True)
    committee3 = models.CharField(max_length=250, blank=True, null=True)
    country3 = models.CharField(max_length=250, blank=True, null=True)
    code = models.CharField(max_length=6, blank=True, null=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    STATUS_CHOICES = [
        ('Unassigned', 'Unassigned'),
        ('Assigned', 'Assigned'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Unassigned')
    captured = models.CharField(max_length=25, blank=True, null=True)

    def __str__(self):
        return self.name

class Committee(models.Model):
    committee = models.CharField(max_length=250)
    countries = models.TextField()  # Store countries as a comma-separated list

    def __str__(self):
        return self.committee

    def get_countries_list(self):
        return [country.strip() for country in self.countries.split(',') if country.strip()]

    

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('Bank Transfer', 'Bank Transfer'),
        ('Portal', 'Portal'),
        ('Remita', 'Remita'),
        ('Cash', 'Cash')
    ]

    AMOUNT_CHOICES = [
        ('Full', 'Full'),
        ('30000', '30,000'),
        ('25000', '25,000'),
    ]

    delegate = models.ForeignKey(Delegate, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.CharField(max_length=6, choices=AMOUNT_CHOICES)
    verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.delegate.name} - {self.payment_method} - {self.amount}"
    

class Assignment(models.Model):
    delegate = models.ForeignKey(Delegate, on_delete=models.CASCADE)
    country = models.CharField(max_length=255)
    committee = models.CharField(max_length=255)
    preference = models.IntegerField()

    def __str__(self):
        return f"{self.delegate.name} - {self.country} - {self.committee}"