from django.shortcuts import render

# Estructura del mapa de procesos extraída del script original
MAP = {
    "GESTIÓN (SGC)": [
        {
            "key": "G1", "name": "Gestión estratégica y política de calidad",
            "purpose": "Dirección y compromiso, objetivos, política, comunicación.",
            "clauses": ["4.1", "4.2", "8.2", "8.3", "8.5", "8.9"],
            "inputs": ["Requisitos de clientes", "Riesgos", "Auditorías"],
            "outputs": ["Política", "Planes", "Mejora"],
            "records": ["SGC-DO-01", "SGC-DO-02", "Actas dirección"],
            "owner": "Dirección / Responsable SGC",
        },
        {
            "key": "G2", "name": "Control documental y de registros",
            "purpose": "Asegurar documentación vigente y control de cambios.",
            "clauses": ["7.5", "8.3"],
            "inputs": ["Documentos", "Normas", "Cambios"],
            "outputs": ["Listado maestro", "Documentos", "Registros"],
            "records": ["Listado maestro", "Historial", "Retención"],
            "owner": "Responsable Documental",
        },
        {
            "key": "G3", "name": "Gestión de riesgos, no conformidades",
            "purpose": "Identificar riesgos, tratar no conformidades y acciones correctivas.",
            "clauses": ["7.10", "8.5", "8.7"],
            "inputs": ["Hallazgos", "Quejas", "Incidentes", "QC"],
            "outputs": ["ACC", "Planes", "Lecciones"],
            "records": ["Registros NC", "Acciones correctivas"],
            "owner": "Calidad / Dirección",
        },
        {
            "key": "G4", "name": "Auditorías internas y revisión por la dirección",
            "purpose": "Evaluar conformidad y eficacia del SGC.",
            "clauses": ["8.8", "8.9"],
            "inputs": ["Programa", "Indicadores", "Resultados"],
            "outputs": ["Informes", "Plan de mejora", "Decisiones"],
            "records": ["Programa auditoría", "Reportes", "Actas"],
            "owner": "Calidad / Dirección",
        },
        {
            "key": "G5", "name": "Gestión de quejas",
            "purpose": "Recepción, investigación y cierre de quejas.",
            "clauses": ["7.9"],
            "inputs": ["Queja cliente", "Evidencias"],
            "outputs": ["Respuesta", "Acciones", "Cierre"],
            "records": ["Registro quejas", "Evidencias", "Cierre"],
            "owner": "Calidad / Atención al cliente",
        },
    ],
    "OPERACIÓN (PROCESOS TÉCNICOS)": [
        {
            "key": "O1", "name": "Revisión de solicitudes y contratos",
            "purpose": "Confirmar alcance, requisitos y método.",
            "clauses": ["7.1"],
            "inputs": ["Solicitud", "Norma", "Capacidad"],
            "outputs": ["Aceptación", "Cotización", "Plan"],
            "records": ["Revisión contrato", "Acuerdos"],
            "owner": "Ventas / Técnico",
        },
        {
            "key": "O2", "name": "Recepción de muestras y trazabilidad",
            "purpose": "Recepción, identificación y custodia.",
            "clauses": ["7.4", "7.8.2"],
            "inputs": ["Muestra", "Instrucciones", "Formato"],
            "outputs": ["Acuse", "Etiqueta", "LIMS"],
            "records": ["Bitácora", "Acuse", "Cadena custodia"],
            "owner": "Recepción",
        },
        {
            "key": "O3", "name": "Preparación, ensayo y medición",
            "purpose": "Ejecución técnica conforme método y condiciones.",
            "clauses": ["6.2", "6.3", "6.4", "6.5", "7.2"],
            "inputs": ["Método", "Muestra", "Equipos", "Ambiente"],
            "outputs": ["Datos crudos", "Resultados"],
            "records": ["Bitácoras", "Registros ambientales"],
            "owner": "Técnico",
        },
        {
            "key": "O4", "name": "Aseguramiento de validez de resultados (QC)",
            "purpose": "Verificación de controles, duplicados, patrones.",
            "clauses": ["7.7"],
            "inputs": ["Datos", "Patrones", "Criterios"],
            "outputs": ["Evidencia QC", "Aprobación"],
            "records": ["Cartas control", "Registros QC"],
            "owner": "Calidad técnica",
        },
        {
            "key": "O5", "name": "Cálculo de incertidumbre",
            "purpose": "Evaluar incertidumbre aplicable y reportarla.",
            "clauses": ["7.6", "7.8.3"],
            "inputs": ["Datos", "Modelo", "Fuentes"],
            "outputs": ["Incertidumbre", "Justificación"],
            "records": ["Hoja incertidumbre", "Supuestos"],
            "owner": "Metrología",
        },
        {
            "key": "O6", "name": "Revisión técnica y emisión de informe",
            "purpose": "Revisión y emisión de reporte ISO.",
            "clauses": ["7.8", "7.2", "7.11"],
            "inputs": ["Resultados", "QC", "Incertidumbre"],
            "outputs": ["Informe", "Entrega"],
            "records": ["Informe", "Registro emisión"],
            "owner": "Responsable técnico",
        },
        {
            "key": "O7", "name": "Gestión de trabajo no conforme",
            "purpose": "Evaluar impacto y decidir acciones sobre repeticiones.",
            "clauses": ["7.10"],
            "inputs": ["Detección NC", "Impacto"],
            "outputs": ["Decisión", "Notificación"],
            "records": ["Registro NC", "Acciones"],
            "owner": "Calidad / Técnico",
        },
    ],
    "SOPORTE (RECURSOS)": [
        {
            "key": "S1", "name": "Competencia y personal",
            "purpose": "Asegurar competencia, formación y autorizaciones.",
            "clauses": ["6.2"],
            "inputs": ["Perfil", "Plan capacitación"],
            "outputs": ["Matriz competencia", "Autorizaciones"],
            "records": ["Matriz", "Evidencias"],
            "owner": "RH / Calidad",
        },
        {
            "key": "S2", "name": "Equipos y mantenimiento",
            "purpose": "Control de equipos, mantenimiento y verificación.",
            "clauses": ["6.4"],
            "inputs": ["Equipo", "Plan Manto", "Calibración"],
            "outputs": ["Equipo apto", "Alertas"],
            "records": ["Inventario", "Certificados"],
            "owner": "Metrología",
        },
        {
            "key": "S3", "name": "Instalaciones y ambiente",
            "purpose": "Mantener y registrar condiciones ambientales.",
            "clauses": ["6.3"],
            "inputs": ["Requisitos", "Monitoreo"],
            "outputs": ["Condiciones controladas", "Registros"],
            "records": ["Bitácora ambiental", "Alarmas"],
            "owner": "Infraestructura",
        },
        {
            "key": "S4", "name": "Compras y servicios externos",
            "purpose": "Evaluar proveedores y compras.",
            "clauses": ["6.6"],
            "inputs": ["Requisición", "Evaluación"],
            "outputs": ["Proveedor aprobado", "Orden compra"],
            "records": ["Lista proveedores", "OC", "Facturas"],
            "owner": "Compras",
        },
        {
            "key": "S5", "name": "Trazabilidad metrológica",
            "purpose": "Asegurar trazabilidad y patrones.",
            "clauses": ["6.5"],
            "inputs": ["Patrones", "Certificados"],
            "outputs": ["Trazabilidad demostrable"],
            "records": ["Certificados", "Verificaciones"],
            "owner": "Metrología",
        },
        {
            "key": "S6", "name": "Control de datos y sistemas",
            "purpose": "Integridad, respaldos y control de acceso.",
            "clauses": ["7.11", "7.5", "8.4"],
            "inputs": ["LIMS", "Backups", "Usuarios"],
            "outputs": ["Datos íntegros", "Recuperación"],
            "records": ["Backups", "Bitácoras", "Controles acceso"],
            "owner": "TI",
        },
    ],
}

def mapa_view(request):
    """
    Vista que envía la estructura del mapa de procesos
    al template web (HTML) para dibujarlo de forma interactiva.
    """
    context = {
        'mapa': MAP
    }
    return render(request, 'a04_mapa_procesos/mapa.html', context)
