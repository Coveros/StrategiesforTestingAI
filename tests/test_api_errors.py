import app.main as main


def test_chat_rejects_missing_json_content_type():
    response = main.app.test_client().post('/api/chat', data='message=test')

    assert response.status_code == 415
    assert response.get_json()['status'] == 'error'


def test_chat_rejects_empty_message():
    response = main.app.test_client().post('/api/chat', json={'message': ' '})

    assert response.status_code == 400
    assert response.get_json()['error'] == 'Empty message provided'


def test_chat_returns_429_when_inference_slot_is_busy():
    assert main._inference_slots.acquire(blocking=False)
    try:
        response = main.app.test_client().post('/api/chat', json={'message': 'test'})
    finally:
        main._inference_slots.release()

    assert response.status_code == 429
    assert response.get_json()['status'] == 'error'


def test_health_returns_503_when_rag_initialization_fails(monkeypatch):
    monkeypatch.setattr(main, 'rag_pipeline', None)
    monkeypatch.setattr(main, 'initialize_rag', lambda: False)

    response = main.app.test_client().get('/api/health')

    assert response.status_code == 503
    assert response.get_json()['status'] == 'unhealthy'