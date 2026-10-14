const API_BASE_URL = 'http://localhost:8000/api';

export async function signInUser(email, password) {
  const resp = await fetch(`${API_BASE_URL}/auth/signin`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  });

  const data = await resp.json().catch(() => ({}));
  if (!resp.ok) {
    throw new Error(data.detail || 'Failed to sign in');
  }

  return data;
}

export async function getCurrentUser(token) {
  const resp = await fetch(`${API_BASE_URL}/auth/me`, {
    headers: { Authorization: `Bearer ${token}` },
  });

  const data = await resp.json().catch(() => ({}));
  if (!resp.ok) {
    throw new Error(data.detail || 'Session expired');
  }

  return data;
}

export async function parseNaturalLanguage(query) {
  const resp = await fetch(`${API_BASE_URL}/travel/parse`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!resp.ok) throw new Error('Failed to parse travel query');
  return resp.json();
}

export async function generatePlanFromNL(query) {
  const resp = await fetch(`${API_BASE_URL}/travel/plan-nl`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ query }),
  });
  if (!resp.ok) throw new Error('Failed to generate travel plan from natural language');
  return resp.json();
}

export async function generatePlanFromForm(formData) {
  const resp = await fetch(`${API_BASE_URL}/travel/plan-form`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(formData),
  });
  if (!resp.ok) throw new Error('Failed to generate travel plan from form');
  return resp.json();
}

export async function getDestinations() {
  const resp = await fetch(`${API_BASE_URL}/travel/destinations`);
  if (!resp.ok) return [];
  return resp.json();
}

export async function getAnalyticsDashboard() {
  const resp = await fetch(`${API_BASE_URL}/analytics/dashboard`);
  if (!resp.ok) throw new Error('Failed to load analytics dashboard');
  return resp.json();
}

export async function saveTripPlan(planData, customTitle) {
  const resp = await fetch(`${API_BASE_URL}/trips/save`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      title: customTitle || `${planData.duration_days}-Day Trip to ${planData.destination}`,
      destination: planData.destination,
      plan_data: planData,
    }),
  });
  if (!resp.ok) throw new Error('Failed to save trip');
  return resp.json();
}

export async function getSavedTrips() {
  const resp = await fetch(`${API_BASE_URL}/trips`);
  if (!resp.ok) return [];
  return resp.json();
}

export async function deleteSavedTrip(tripId) {
  const resp = await fetch(`${API_BASE_URL}/trips/${tripId}`, {
    method: 'DELETE',
  });
  if (!resp.ok) throw new Error('Failed to delete saved trip');
  return resp.json();
}

export async function sendChatMessage(message, currentPlan, conversationHistory = []) {
  const resp = await fetch(`${API_BASE_URL}/chat/`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({
      message,
      current_plan: currentPlan,
      conversation_history: conversationHistory,
    }),
  });
  if (!resp.ok) throw new Error('Chat assistant error');
  return resp.json();
}
