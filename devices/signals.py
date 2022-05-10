from django.dispatch import Signal

# This signal is created as a practice for custom signals
# Other wise OOTB post-save can also be used
custom_post_save = Signal()
