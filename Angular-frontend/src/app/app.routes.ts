import { Routes } from '@angular/router';
import { LoginPageComponent } from './pages/login-page/login-page.component';
import { RegisterPageComponent } from './pages/register-page/register-page.component';
import { BooksPageComponent } from './pages/books-page/books-page.component';
import { BookDetailPageComponent } from './pages/book-detail-page/book-detail-page.component';
import { ReservationsPageComponent } from './pages/reservations-page/reservations-page.component';
import { BorrowsPageComponent } from './pages/borrows-page/borrows-page.component';
import { AdminPageComponent } from './pages/admin-page/admin-page.component';
import { authGuard } from './guards/auth.guard';
import { adminGuard } from './guards/admin.guard';

export const routes: Routes = [
  { path: '', redirectTo: '/books', pathMatch: 'full' },
  { path: 'login', component: LoginPageComponent },
  { path: 'register', component: RegisterPageComponent },
  { path: 'books', component: BooksPageComponent, canActivate: [authGuard] },
  { path: 'books/:id', component: BookDetailPageComponent, canActivate: [authGuard] },
  { path: 'reservations', component: ReservationsPageComponent, canActivate: [authGuard] },
  { path: 'borrows', component: BorrowsPageComponent, canActivate: [authGuard] },
  { path: 'admin', component: AdminPageComponent, canActivate: [authGuard, adminGuard] },
  { path: '**', redirectTo: '/books' }
];

