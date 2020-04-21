const API_URL = Cypress.env('API_URL')
const HOST = Cypress.env('HOST')

describe('superadmin\'s product types list', function () {
  /* auth */
  beforeEach(function (done) {
    cy.customLogin(done)
  })

  it('Can access product types page', function () {
    cy.visit('/admin/product_types')
    cy.url().should('eq', `${HOST}/admin/product_types`)
  })

  it('There are product types on product types list page', function () {
    cy.get('[data-cy="ProductTypeItem"]').should('exist')
  })

  it('There is "add new product type" button visible on the page', function () {
    cy.get('[data-cy="AddProductTypeItemButton"]').should('exist')
  })

  it('Click on "add new" leads to /add url', function () {
    cy.get('[data-cy="AddProductTypeItemButton"]').click()
    cy.url().should('eq', `${HOST}/admin/product_types/add`)
  })
})
