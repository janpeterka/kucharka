describe('try unlogged things',() => {
  it('shows public index', () => {
      cy.visit('http://127.0.0.1:5000/')
      cy.get('body').should('contain', 's čím ti pomůže?')
  })

  it('doesn\'t show recipes', () => {
      cy.visit('http://127.0.0.1:5000/recipe/')
      cy.get('body').should('contain', 'přihlásit se')
  })

  it('can register', () => {
      cy.visit('http://127.0.0.1:5000/register')
      cy.get('body').should('contain', 'zaregistrovat se')
      cy.get('input#email').type('admin@skautskakucharka.cz')
      cy.get('input#password').type('kucharky')
      cy.get('input#password_confirm').type('kucharky')
      cy.get('input#submit').click()
      cy.get('body').should('contain', 'vítej!')
  })

  it('can logout', () => {
      cy.visit('http://127.0.0.1:5000/logout')
      cy.get('body').should('contain', 's čím ti pomůže?')
  })

  it('can\'t register with existing', () => {
      cy.visit('http://127.0.0.1:5000/register')
      cy.get('body').should('contain', 'zaregistrovat se')
      cy.get('input#email').type('admin@skautskakucharka.cz')
      cy.get('input#password').type('kucharky')
      cy.get('input#password_confirm').type('kucharky')
      cy.get('input#submit').click()
      cy.get('body').should('contain', 'already associated')
  })

  it('can login', () => {
      cy.visit('http://127.0.0.1:5000/login')
      cy.get('body').should('contain', 'přihlásit se')
      cy.get('input#email').type('admin@skautskakucharka.cz')
      cy.get('input#password').type('kucharky')
      cy.get('input#submit').click()
      cy.get('body').should('contain', 'vítej!')
  })

  // TODO:
  // - login with Google OAuth
  // - solve testing registration (probably somehow using testing env for this)


})
