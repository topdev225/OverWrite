const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

describe('superadmin\'s orders list', function () {
  /* auth */
  beforeEach(function () {
    cy.customLogin();
  })

  it('Can access orders page', function () {
    cy.visit('/admin/orders')
  })
})
