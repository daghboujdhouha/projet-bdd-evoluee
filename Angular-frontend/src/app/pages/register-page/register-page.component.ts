import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-register-page',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  template: `
    <div class="card" style="max-width: 400px; margin: 50px auto;">
      <h2>Inscription</h2>
      <form (ngSubmit)="onSubmit()">
        <div class="form-group">
          <label for="username">Nom d'utilisateur</label>
          <input type="text" id="username" [(ngModel)]="username" name="username" required>
        </div>
        <div class="form-group">
          <label for="email">Email</label>
          <input type="email" id="email" [(ngModel)]="email" name="email" required>
        </div>
        <div class="form-group">
          <label for="password">Mot de passe</label>
          <input type="password" id="password" [(ngModel)]="password" name="password" required>
        </div>
        <div class="form-group">
          <label for="role">Rôle</label>
          <select id="role" [(ngModel)]="role" name="role" required>
            <option value="etudiant">Étudiant</option>
            <option value="enseignant">Enseignant</option>
          </select>
        </div>
        <div *ngIf="error" class="alert alert-error">
          {{ error }}
        </div>
        <button type="submit" class="btn btn-primary" [disabled]="loading">
          {{ loading ? "Inscription..." : "S'inscrire" }}
        </button>
      </form>
      <p style="margin-top: 20px; text-align: center;">
        Déjà un compte ? <a routerLink="/login">Se connecter</a>
      </p>
    </div>
  `,
  styles: []
})
export class RegisterPageComponent {
  username = '';
  email = '';
  password = '';
  role = 'etudiant';
  error = '';
  loading = false;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  onSubmit(): void {
    this.error = '';
    this.loading = true;

    this.authService.register(this.username, this.email, this.password, this.role).subscribe({
      next: () => {
        this.router.navigate(['/books']);
      },
      error: (err) => {
        this.error = err.error?.error || 'Erreur lors de l\'inscription';
        this.loading = false;
      }
    });
  }
}

