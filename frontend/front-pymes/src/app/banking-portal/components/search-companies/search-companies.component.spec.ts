import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SearchCompaniesComponent } from './search-companies.component';

describe('SearchCompaniesComponent', () => {
  let component: SearchCompaniesComponent;
  let fixture: ComponentFixture<SearchCompaniesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SearchCompaniesComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SearchCompaniesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
