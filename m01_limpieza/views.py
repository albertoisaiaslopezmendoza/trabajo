from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import ActivoLimpieza, RegistroLimpieza
from .utils import calcular_estatus, generar_pdf_evidencia


@login_required
def m01_dashboard(request):
    registros = RegistroLimpieza.objects.all()[:20]
    context = {'registros': registros}

    if request.method == 'POST':
        accion = request.POST.get('accion')

        if accion == 'buscar':
            codigo = request.POST.get('codigo_barras', '').strip()
            activo = ActivoLimpieza.objects.filter(codigo_barras=codigo).first()

            if activo:
                # Lógica para mostrar las tareas en el HTML
                # Asumimos que en el admin las escribes una por línea
                lista_tareas = []
                if activo.checklist_default:
                    lista_tareas = activo.checklist_default.splitlines()

                activo.checklist_lista = lista_tareas
                context['activo_encontrado'] = activo
                context['codigo_preservado'] = codigo
                messages.success(request, f"Activo cargado: {activo.nombre}")
            else:
                messages.error(request, f"Código '{codigo}' no encontrado.")

        elif accion == 'guardar':
            codigo = request.POST.get('codigo_preservado')
            activo = ActivoLimpieza.objects.filter(codigo_barras=codigo).first()

            if activo:
                # 1. Obtener la lista de checkbox marcados
                checklist_hecho_lista = request.POST.getlist('check_item')

                # 2. CONVERTIR A TEXTO SIMPLE (Separado por comas)
                # Ejemplo resultado: "Barrer, Trapear, Limpiar Mesas"
                checklist_texto = ", ".join(checklist_hecho_lista)

                # 3. Obtener químicos (ya es texto)
                quimicos_texto = request.POST.get('quimicos', '')

                estado_calc, proximo = calcular_estatus(timezone.now(), activo.frecuencia_dias)

                registro = RegistroLimpieza.objects.create(
                    activo_relacionado=activo,
                    nombre_activo_snapshot=activo.nombre,
                    area_snapshot=activo.area,
                    realizado_por=request.user,
                    tipo_limpieza=request.POST.get('tipo', 'RUTINA'),
                    frecuencia_aplicada=activo.frecuencia_dias,
                    estado=estado_calc,
                    proximo_vencimiento=proximo,
                    checklist_realizado=checklist_texto,  # Guardamos TEXTO PURO
                    quimicos_usados=quimicos_texto,  # Guardamos TEXTO PURO
                    observaciones=request.POST.get('observaciones', '')
                )

                # Generar PDF
                pdf = generar_pdf_evidencia(registro)
                registro.evidencia_pdf.save(f"evidencia_{registro.uuid}.pdf", pdf)
                registro.save()

                messages.success(request, "Limpieza registrada correctamente (Texto Plano).")
                return redirect('m01_dashboard')
            else:
                messages.error(request, "Error: Se perdió la referencia del activo.")

    return render(request, 'm01_limpieza/dashboard.html', context)