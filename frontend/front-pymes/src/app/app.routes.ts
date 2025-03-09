import { Routes } from '@angular/router';
import { LoginComponent } from './authentication/components/login/login.component';
import { DashboardComponent } from './shared-elements/components/dashboard/dashboard.component';
import { SumaryOptionsComponent } from './shared-elements/components/sumary-options/sumary-options.component';
import { SearchCompaniesComponent } from './banking-portal/components/search-companies/search-companies.component';
import { ListCertificationsComponent } from './certifications/components/list-certifications/list-certifications.component';
import { ListCompaniesComponent } from './contacts-network/components/list-companies/list-companies.component';
import { InfoSummaryTrustComponent } from './financing/components/info-summary-trust/info-summary-trust.component';

export const routes: Routes = [
    { path: '', redirectTo: 'authentication', pathMatch: 'full' },
    //Authentication module routes
    {
        path: 'authentication',
        children: [
            { path: 'login', component: LoginComponent },
            { path: '', redirectTo: 'login', pathMatch: 'full' },
        ]
    },
    //PYME module routes
    {
        path: 'pyme',
        children: [
            {
                path: 'dashboard', component: DashboardComponent,
                children: [
                    { path: 'options', component: SumaryOptionsComponent },
                    { path: 'banking-portal', component: SearchCompaniesComponent },
                    { path: 'certifications', component: ListCertificationsComponent },
                    { path: 'financing', component: InfoSummaryTrustComponent },
                    { path: 'contacts-network', component: ListCompaniesComponent },
                    { path: '', redirectTo: 'options', pathMatch: 'full' },
                ]
            }
        ]
    }
];
