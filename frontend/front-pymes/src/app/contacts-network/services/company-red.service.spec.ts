import { TestBed } from '@angular/core/testing';

import { CompanyRedService } from './company-red.service';

describe('CompanyRedService', () => {
  let service: CompanyRedService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(CompanyRedService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
