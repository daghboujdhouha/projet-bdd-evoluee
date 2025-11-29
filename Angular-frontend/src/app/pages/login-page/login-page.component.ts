import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="card" style="max-width: 400px; margin: 50px auto;">
      <h2>Connexion</h2>
      <form (ngSubmit)="onSubmit()">
        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input type="text" id="username" [(ngModel)]="username" name="username" required>
        </div>
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input type="password" id="password" [(ngModel)]="password" name="password" required>
        </div>
        <div *ngIf="error" class="alert alert-error">
          {{ error }}
        </div>
        <button type="submit" class="btn btn-primary" [disabled]="loading">
          {{ loading ? 'Connexion...' : 'Se connecter' }}
        </button>
      </form>
      <p style="margin-top: 20px; text-align: center;">
        Pas encore de compte ? <a routerLink="/register">S'inscrire</a>
      </p>
    </div>
  `,
  styles: []
})
export class LoginPageComponent {
  username = '';
  password = '';
  error = '';
  loading = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    this.error = '';
    this.loading = true;

    this.authService.login(this.username, this.password).subscribe({
      next: () => {
        this.router.navigate(['/books']);
      },
      error: (err) => {
        this.error = err.error?.error || 'Erreur de connexion';
        this.loading = false;
      }
    });
  }
}

