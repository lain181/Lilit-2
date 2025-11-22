from django.shortcuts import render

def test1(request):
    return render(request,'posts/test1.html')