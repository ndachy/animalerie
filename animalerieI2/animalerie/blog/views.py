from django.shortcuts import render, get_object_or_404, redirect
from .forms import MoveForm
from .models import Animal, Equipement






def animal_list(request):
    animaux = Animal.objects.all()
    equipements = Equipement.objects.all()
    return render(request, 'blog/animal_list.html', {"animaux" : animaux, "equipements" : equipements} )



def animal_detail(request, id_animal):
    
    mangeoire = get_object_or_404(Equipement, id_equip='mangeoire')
    marelle = get_object_or_404(Equipement, id_equip='marelle')
    nid = get_object_or_404(Equipement, id_equip='nid')
    litière = get_object_or_404(Equipement, id_equip='litière')
    animal = get_object_or_404(Animal, id_animal=id_animal)
    ancien_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
    if request.method == "POST":
        form = MoveForm(request.POST, instance=animal)
        if form.is_valid():
            if form.data['lieu'] == 'mangeoire':
                if mangeoire.disponibilite == 'occupé':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': "la mangeoire est occupée"})
                elif animal.etat == 'affamé' and mangeoire.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'repus'
                    form.save()                  
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "occupé"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')                
                else:
                    if ancien_lieu!= litière:
                        ancien_lieu.disponibilite = "occupé"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"{animal} n'a pas faim"})

            elif form.data['lieu'] == 'marelle':
                if marelle.disponibilite == 'occupé':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"La marelle est occupée"})            
                elif animal.etat == 'repus' and marelle.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'fatigué'
                    form.save()
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "occupé"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')   
                else:
                    if ancien_lieu!= litière:
                        ancien_lieu.disponibilite = "occupé"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"{animal} n'est pas repus"})

            elif form.data['lieu'] == 'nid':
                if nid.disponibilite == 'occupé':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Ca dort encore..."})            
                elif animal.etat == 'fatigué' and nid.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'endormi'
                    form.save()
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "occupé"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')                       
                else:
                    if ancien_lieu!= litière:
                        ancien_lieu.disponibilite = "occupé"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"{animal} n'est pas fatigué"})

            elif form.data['lieu'] == 'litière':
                if litière.disponibilite == 'occupé':
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"Quelqu'un est déjà aux toilettes"})              
                elif animal.etat == 'endormi' and litière.disponibilite == 'libre':
                    ancien_lieu.disponibilite = "libre"
                    ancien_lieu.save()
                    animal.etat = 'affamé'
                    form.save()
                    nouveau_lieu = get_object_or_404(Equipement, id_equip=animal.lieu)
                    nouveau_lieu.disponibilite = "libre"
                    nouveau_lieu.save()
                    animal.save()
                    return redirect('animal_list')                       
                else:
                    if ancien_lieu!= litière:
                        ancien_lieu.disponibilite = "occupé"
                        ancien_lieu.save()
                        form.save(commit=False)
                    return render(request ,"blog/animal_detail.html", {'animal': animal, 'message': f"{animal} est debout"})


                  
        else:
            form = MoveForm()
    else:
        form = MoveForm()

    return render(request, 'blog/animal_detail.html', {'animal': animal, 'lieu': animal.lieu, 'form': form})

def equipement_detail(request, id_equip):
    equipement = get_object_or_404(Equipement, id_equip=id_equip)
    animaux = Animal.objects.all()
    for animal in animaux:
        if animal.lieu == equipement:
            return render(request, 'blog/equipement_detail.html', {"equipement" : equipement, "animal": animal})        
    return render(request, 'blog/equipement_detail.html', {"equipement" : equipement})