import { ComponentFixture, TestBed } from '@angular/core/testing';

import { InfoSummaryTrustComponent } from './info-summary-trust.component';

describe('InfoSummaryTrustComponent', () => {
  let component: InfoSummaryTrustComponent;
  let fixture: ComponentFixture<InfoSummaryTrustComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [InfoSummaryTrustComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(InfoSummaryTrustComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
