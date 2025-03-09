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
      name: "Certificación Financiera",
      shortDescription: "Validación de salud financiera",
      progress: 100,
      largeDescription: "Esta certificación valida la salud financiera de tu empresa basada en estados financieros y flujo de caja.",
      details: {
        requirements: "Presentar estados financieros de los últimos dos años, Declaraciones de impuestos al día y Análisis de solvencia y rentabilidad. ",
        benefits: "Acceso a líneas de crédito con mejores tasas, Mayor confianza para proveedores e inversionistas, Posibilidad de participar en licitaciones públicas y privadas, etc"
      }
    },
    {
      name: "Certificación Operativa",
      shortDescription: "Validación de procesos operativos",
      progress: 35,
      largeDescription: "React es una librería de JavaScript que permite desarrollar aplicaciones web de una forma más sencilla y rápida.",
      details: {
        requirements: "Presentar estados financieros de los últimos dos años, Declaraciones de impuestos al día y Análisis de solvencia y rentabilidad. ",
        benefits: "Acceso a líneas de crédito con mejores tasas, Mayor confianza para proveedores e inversionistas, Posibilidad de participar en licitaciones públicas y privadas, etc"
      }
    },
    {
      name: "Certificación Fiscal",
      shortDescription: "Esta certificación valida el cumplimiento de obligaciones fiscales y transparencia tributaria.",
      progress: 0,
      largeDescription: "Vue es un framework de JavaScript que permite desarrollar aplicaciones web de una forma más sencilla y rápida.",
      details: {
        requirements: "Presentar estados financieros de los últimos dos años, Declaraciones de impuestos al día y Análisis de solvencia y rentabilidad. ",
        benefits: "Acceso a líneas de crédito con mejores tasas, Mayor confianza para proveedores e inversionistas, Posibilidad de participar en licitaciones públicas y privadas, etc"
      }
    }
  ]
}
