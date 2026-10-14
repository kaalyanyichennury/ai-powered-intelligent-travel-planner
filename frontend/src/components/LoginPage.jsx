import { useState } from 'react';
import {
  ArrowRight,
  Check,
  Compass,
  Eye,
  EyeOff,
  Globe2,
  LockKeyhole,
  Mail,
  MapPin,
  ShieldCheck,
  Sparkles,
} from 'lucide-react';
import './LoginPage.css';

export default function LoginPage({ onContinueAsGuest, onSignIn }) {
  const [showPassword, setShowPassword] = useState(false);
  const [notice, setNotice] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (event) => {
    event.preventDefault();
    const trimmedEmail = email.trim();
    const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    if (!trimmedEmail) {
      setNotice('Please enter your email to sign in.');
      return;
    }

    if (!emailPattern.test(trimmedEmail)) {
      setNotice('Please enter a valid email address.');
      return;
    }

    if (!password) {
      setNotice('Please enter your password to sign in.');
      return;
    }

    setNotice('Signing in...');
    setIsSubmitting(true);

    try {
      await onSignIn?.(trimmedEmail, password);
    } catch (error) {
      setNotice(error?.message || 'Unable to sign in right now. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <main className="login-page">
      <section className="login-showcase" aria-label="Travel inspiration">
        <div className="login-showcase__image" />
        <div className="login-showcase__shade" />
        <div className="login-showcase__content">
          <a className="login-brand login-brand--light" href="#" onClick={(event) => event.preventDefault()}>
            <span className="login-brand__mark"><Compass size={21} strokeWidth={1.8} /></span>
            <span>AeroVoyage<span className="login-brand__accent"> AI</span></span>
          </a>

          <div className="login-story">
            <span className="login-eyebrow"><Sparkles size={14} /> YOUR NEXT CHAPTER STARTS HERE</span>
            <h1>Go beyond<br />the <em>ordinary.</em></h1>
            <p>Thoughtful itineraries, made for the way you want to see the world.</p>
          </div>

          <div className="login-place-card">
            <span className="login-place-card__icon"><MapPin size={16} /></span>
            <span>
              <strong>Somewhere unforgettable</strong>
              <small>Your next favorite place is waiting.</small>
            </span>
            <span className="login-place-card__dots"><i /><i /><i /></span>
          </div>
          <span className="login-photo-credit">A little inspiration for the road ahead</span>
        </div>
      </section>

      <section className="login-panel">
        <div className="login-panel__top">
          <div className="login-panel__mobile-brand">
            <span className="login-brand__mark"><Compass size={20} strokeWidth={1.8} /></span>
            <span>AeroVoyage<span className="login-brand__accent"> AI</span></span>
          </div>
          <span className="login-secure"><ShieldCheck size={14} /> PRIVATE & SECURE</span>
        </div>

        <div className="login-content">
          <div className="login-welcome-icon"><Globe2 size={22} strokeWidth={1.7} /></div>
          <span className="login-eyebrow login-eyebrow--dark">WELCOME TO AEROVOYAGE</span>
          <h2>Let's get you<br />going places.</h2>
          <p className="login-intro">Sign in to pick up where your travel story left off.</p>

          <form className="login-form" onSubmit={handleSubmit}>
            <label htmlFor="login-email">Email address</label>
            <div className="login-input-wrap">
              <Mail size={17} aria-hidden="true" />
              <input
                id="login-email"
                name="email"
                type="email"
                placeholder="you@example.com"
                autoComplete="email"
                required
                value={email}
                onChange={(event) => setEmail(event.target.value)}
              />
            </div>

            <div className="login-label-row">
              <label htmlFor="login-password">Password</label>
              <button
                className="login-text-button"
                type="button"
                onClick={() => setNotice('Password recovery will be available when sign-in is connected.')}
              >
                Forgot password?
              </button>
            </div>
            <div className="login-input-wrap">
              <LockKeyhole size={17} aria-hidden="true" />
              <input
                id="login-password"
                name="password"
                type={showPassword ? 'text' : 'password'}
                placeholder="Enter your password"
                autoComplete="current-password"
                required
                value={password}
                onChange={(event) => setPassword(event.target.value)}
              />
              <button
                className="login-password-toggle"
                type="button"
                aria-label={showPassword ? 'Hide password' : 'Show password'}
                onClick={() => setShowPassword((visible) => !visible)}
              >
                {showPassword ? <EyeOff size={17} /> : <Eye size={17} />}
              </button>
            </div>

            <label className="login-remember">
              <input type="checkbox" name="remember" />
              <span className="login-checkbox"><Check size={12} /></span>
              <span>Keep me signed in</span>
            </label>

            {notice && <p className="login-notice" role="status">{notice}</p>}

            <button className="login-submit" type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Signing in...' : 'Sign in'} <ArrowRight size={17} />
            </button>
          </form>

          <div className="login-divider"><span>NEW TO AEROVOYAGE?</span></div>
          <button className="login-guest" type="button" onClick={onContinueAsGuest}>
            Explore as a guest <ArrowRight size={16} />
          </button>
          <p className="login-terms">By continuing, you agree to our <a href="#terms" onClick={(event) => event.preventDefault()}>Terms</a> and <a href="#privacy" onClick={(event) => event.preventDefault()}>Privacy Policy</a>.</p>
        </div>

        <div className="login-panel__footer">
          <span>© 2026 AeroVoyage AI</span>
          <span>Made for curious minds <Sparkles size={13} /></span>
        </div>
      </section>
    </main>
  );
}
