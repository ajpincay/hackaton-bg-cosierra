import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SumaryOptionsComponent } from './sumary-options.component';

describe('SumaryOptionsComponent', () => {
  let component: SumaryOptionsComponent;
  let fixture: ComponentFixture<SumaryOptionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [SumaryOptionsComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(SumaryOptionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
