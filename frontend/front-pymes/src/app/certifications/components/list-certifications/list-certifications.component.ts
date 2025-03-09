import { Component } from '@angular/core';
import { InfoCertificationComponent } from "../info-certification/info-certification.component";
import { certificationsI } from '../../interfaces/certifications';

@Component({
  selector: 'app-list-certifications',
  imports: [InfoCertificationComponent],
  templateUrl: './list-certifications.component.html',
  styleUrl: './list-certifications.component.css'
})
export class ListCertificationsComponent {
  //Variables
  arrayCertifications: certificationsI[] = [
    {
      name: "Certificación de Procesos",
      shortDescription: "Procesos y controles de su empresa",
      progress: 100,
      largeDescription: "Verifica que los procesos empresariales cumplen estándares de calidad y eficiencia",
      details: {
        requirements: "Presentar estados financieros de los últimos dos años, Declaraciones de impuestos al día y Análisis de solvencia y rentabilidad. ",
        benefits: "Acceso a líneas de crédito con mejores tasas, Mayor confianza para proveedores e inversionistas, Posibilidad de participar en licitaciones públicas y privadas, etc"
      }
    },
    {
      name: "Certificación de idoneidad",
      shortDescription: "Validación de procesos de idoneidad",
      progress: 35,
      largeDescription: "Asegura que la empresa cumple requisitos legales y operativos para su actividad.",
      details: {
        requirements: "Presentar estados financieros de los últimos dos años, Declaraciones de impuestos al día y Análisis de solvencia y rentabilidad. ",
        benefits: "Acceso a líneas de crédito con mejores tasas, Mayor confianza para proveedores e inversionistas, Posibilidad de participar en licitaciones públicas y privadas, etc"
      }
    },
    {
      name: "Certificación de tecnología",
      shortDescription: "Valida el uso de equipo tecnológico de su negocio",
      progress: 0,
      largeDescription: "Valida la seguridad y eficiencia de los sistemas tecnológicos de la empresa",
      details: {
        requirements: "Presentar estados financieros de los últimos dos años, Declaraciones de impuestos al día y Análisis de solvencia y rentabilidad. ",
        benefits: "Acceso a líneas de crédito con mejores tasas, Mayor confianza para proveedores e inversionistas, Posibilidad de participar en licitaciones públicas y privadas, etc"
      }
    },
    {
      name: "Auditorías",
      shortDescription: "Comprobación de la transparencia de su empresa",
      progress: 0,
      largeDescription: "Evalúan la transparencia financiera, operativa y de gestión de la empresa.",
      details: {
        requirements: "Presentar estados financieros de los últimos dos años, Declaraciones de impuestos al día y Análisis de solvencia y rentabilidad. ",
        benefits: "Acceso a líneas de crédito con mejores tasas, Mayor confianza para proveedores e inversionistas, Posibilidad de participar en licitaciones públicas y privadas, etc"
      }
    }
  ]
}
