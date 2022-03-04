describe('try unlogged things',() => {
  it('shows dashboard', () => {
      cy.visit('http://127.0.0.1:5000/')
      cy.get('body').should('contain', 'Vítejte na stránkách skautské kuchařky.')
  })

  it('can login', () => {
      cy.visit('http://127.0.0.1:5000/login')
      cy.get('body').should('contain', 'Přihlásit se')
      cy.get('input#email').type('admin@admin.cz')
      cy.get('input#password').type('mainframe')
      cy.get('input#submit').click()
      cy.get('body').should('contain', 'Vítejte!')
  })

  it('can not register with existing', () => {
      cy.visit('http://127.0.0.1:5000/register')
      cy.get('body').should('contain', 'Zaregistrovat se')
      cy.get('input#email').type('admin@admin.cz')
      cy.get('input#password').type('mainframe')
      cy.get('input#password_confirm').type('mainframe')
      cy.get('input#submit').click()
      cy.get('body').should('contain', 'Vítejte!')
  })

  it('can register', () => {
      cy.visit('http://127.0.0.1:5000/register')
      cy.get('body').should('contain', 'Přihlásit se')
      cy.get('input#email').type('admin@admin.cz')
      cy.get('input#password').type('mainframe')
      cy.get('input#submit').click()
      cy.get('body').should('contain', 'Vítejte!')
  })


})
