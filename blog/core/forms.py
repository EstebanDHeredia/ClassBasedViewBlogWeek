from django import forms
from .models import Post, Category

# Creo la clase que me va a generar el formulario que voy a utilizar para crear un nuevo
# post desde el frontend. Va a ser un Model Based Form
class PostForm(forms.ModelForm):
    
    class Meta:
        model = Post
        # Indico los campos del modelo Post que quiero mostrar en el formulario:
        fields = ['title', 'excerpt', 'content', 'image', 'category', 'tags']

        # Indico con qué widgets quiero que me muestre los campos en el formulario en el front.
        # Otra alternativa podría haber sido utilizar CrispyForms
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'excerpt': forms.Textarea(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.SelectMultiple(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Filtrar las categorías activas en el formulario
        self.fields['category'].queryset = Category.objects.filter(active=True)

